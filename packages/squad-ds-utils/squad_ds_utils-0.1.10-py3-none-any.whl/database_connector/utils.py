import boto3
import json

from cachetools import cached, TTLCache
ssm_client = boto3.client('ssm', region_name='us-east-1')


@cached(cache=TTLCache(maxsize=32, ttl=60))
def get_parameter(parameter_name: str) -> str:
    """
    Fetches the value of the given parameter from AWS SSM Parameter Store.
    :param parameter_name: String
    :return: String
    """
    return ssm_client.get_parameter(
        Name=parameter_name, WithDecryption=True
    )['Parameter']['Value']


@cached(cache=TTLCache(maxsize=32, ttl=60))
def get_parameters(parameter_names: [str], region='us-east-1') -> {str: str}:
    """
    Fetches the given parameters from SSM Parameter store.
    :param parameter_names: List of strings
    :param region: String
    :return: dictionary containing key-value pairs
    """
    ssm_client = boto3.client('ssm', region_name=region)

    parameters = ssm_client.get_parameters(
        Names=parameter_names, WithDecryption=True
    )['Parameters']

    parameter_to_value_map = {
        parameter['Name']: parameter['Value']
        for parameter in parameters
    }

    return parameter_to_value_map


@cached(cache=TTLCache(maxsize=32, ttl=60))
def get_secret_value(secret_name: str, region='ap-south-1') -> str:
    """
    Fetches the value of the given parameter from AWS Secret Manager.
    :param secret_name: String
    :return: String
    """
    secretsmanager_client = boto3.client('secretsmanager', region_name=region)

    response = secretsmanager_client.get_secret_value(SecretId=secret_name)

    # Access the secret value
    return json.loads(response['SecretString'])
