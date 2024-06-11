# region
AWS_REGION = "ap-south-1"

# postgres's parameter store
SAGEMAKER_PG_DB_NAME_PARAMETER = "squadiq-sagemaker-pg-db-name"
SAGEMAKER_PG_USERNAME_PARAMETER = "squadiq-sagemaker-pg-username"
SAGEMAKER_PG_PASSWORD_PARAMETER = "squadiq-sagemaker-pg-password"
SAGEMAKER_PG_HOST_PARAMETER = "squadiq-sagemaker-pg-host"

# snowflake's parameter store
SNOWFLAKE_ACCOUNT_NAME_PARAMETER = "snowflake-account-name-parameter"
SNOWFLAKE_WAREHOUSE_NAME_PARAMETER = "snowflake-warehouse-name-parameter"

SAGEMAKER_RESOURCE_PATH = '/opt/ml/metadata/resource-metadata.json'
SAGEMAKER_SSL_CERT_PATH= "./rds_certificate.pem"
