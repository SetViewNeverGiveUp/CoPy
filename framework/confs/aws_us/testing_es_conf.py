from lib_secrets_manager import *
secrets_manager = SecretsManager()
secrets = secrets_manager.getSecretValue('elasticsearch')
TESTING_ES_HOST = "xxxxxxxxxxxxx"
TESTING_ES_SCHEME = "https"
TESTING_ES_PORT = "443"
TESTING_ES_USER = secrets['user']
TESTING_ES_PASSWORD = secrets['password']