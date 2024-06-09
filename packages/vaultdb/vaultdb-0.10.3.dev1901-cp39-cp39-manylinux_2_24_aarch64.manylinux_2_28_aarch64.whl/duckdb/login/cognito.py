import os
from ..duckdb import DuckDBPyConnection

# Set up the logger
import logging


def cognito(username: str, password: str, path: str=":memory:", aws_region: str='us-east-2', **userpoolargs)->DuckDBPyConnection:
    import boto3
    import duckdb
    logger = logging.getLogger()
    connection = duckdb.connect(path, False)
    if userpoolargs:
        USER_POOL_ID = userpoolargs["USER_POOL_ID"]
        USER_POOL_APP_CLIENT_ID = userpoolargs["USER_POOL_APP_CLIENT_ID"]
        USER_IDENTITY_POOL_ID = userpoolargs["USER_IDENTITY_POOL_ID"]
        if "USER_BUCKET" in userpoolargs:
            USER_BUCKET = userpoolargs["USER_BUCKET"]
            connection.execute(
                f"CREATE OR REPLACE CONFIG remote_merge_path AS 's3://{USER_BUCKET}';"
            )
        connection.execute(f"CREATE OR REPLACE CONFIG user_pool_id AS '{USER_POOL_ID}';")
        connection.execute(
            f"CREATE OR REPLACE CONFIG user_pool_client_id AS '{USER_POOL_APP_CLIENT_ID}';"
        )
        connection.execute(
            f"CREATE OR REPLACE CONFIG identity_pool_id AS '{USER_IDENTITY_POOL_ID}';"
        )

    configs = connection.execute(
        "select config_name, config_value from vaultdb_configs"
    ).fetchall()
    if not configs:
        raise Exception("Config Data Not found in Database")

    configs = dict(configs)
    user_pool_client_id = configs["user_pool_client_id"]
    user_pool_id = configs["user_pool_id"]
    identity_pool_id = configs["identity_pool_id"]
    region = identity_pool_id.split(":")[0]

    client = boto3.client("cognito-idp", region_name=region)
    # Initiating the Authentication,
    response = client.initiate_auth(
        ClientId=user_pool_client_id,
        AuthFlow="USER_PASSWORD_AUTH",
        AuthParameters={"USERNAME": username, "PASSWORD": password},
    )

    # From the JSON response you are accessing the AccessToken
    logger.debug(response)
    # Getting the user details.
    # access_token = response["AuthenticationResult"]["AccessToken"]
    id_token = response["AuthenticationResult"]["IdToken"]

    identity = boto3.client("cognito-identity", region_name=region)
    response = identity.get_id(
        IdentityPoolId=identity_pool_id,
        Logins={f"cognito-idp.{region}.amazonaws.com/{user_pool_id}": id_token},
    )
    logger.debug(response)
    identityId = response["IdentityId"]

    response = identity.get_credentials_for_identity(
        IdentityId=identityId,
        Logins={f"cognito-idp.{region}.amazonaws.com/{user_pool_id}": id_token},
    )

    logger.debug(response)
    aws_cred = response["Credentials"]
    connection.execute(
        f"CREATE OR REPLACE SECRET {username} (TYPE S3, PROVIDER config, KEY_ID '{aws_cred['AccessKeyId']}', SECRET '{aws_cred['SecretKey']}', REGION '{aws_region}', SESSION_TOKEN '{aws_cred['SessionToken']}')"
    )
    # duckdb_secrets = connection.execute("select * from duckdb_secrets();").fetch_df()
    # print(duckdb_secrets.head(5))
    return connection


if __name__ == "__main__":
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)  # Very verbose
    connection = cognito (
        "vaultdb",
        "test123",
        path=":memory:",
        USER_POOL_ID="XXXXXXXXXXX",
        USER_POOL_APP_CLIENT_ID="XXXXXXXXXXXXXXXXXXXXX",
        USER_IDENTITY_POOL_ID="XXXXXXXXXXXXXXXXXXXXXXXXXXXX",
        USER_BUCKET="XXXXXXXXXXXXXXXXXXXXXXXXX"
    )
