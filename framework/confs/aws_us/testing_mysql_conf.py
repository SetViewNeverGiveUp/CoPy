from lib_secrets_manager import *
secrets_manager = SecretsManager()
secrets = secrets_manager.getSecretValue('mysql_data')

TESTING_MYSQL_HOST = "xxxxxxxxxxxxxx"
TESTING_MYSQL_PORT = "3380"
TESTING_MYSQL_USER = secrets['user']
TESTING_MYSQL_PWD = secrets['password']

TESTING_MYSQL_NAME="co_TESTING"
TESTING_MYSQL_CHARSET="utf8"
TESTING_MYSQL_PREFIX="TESTING_"