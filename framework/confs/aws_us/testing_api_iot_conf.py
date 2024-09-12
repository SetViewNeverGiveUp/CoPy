from lib_secrets_manager import *
secrets_manager = SecretsManager()
secrets = secrets_manager.getSecretValue('api_iot')
TESTING_API_IOT_URL = 'https://xxxxxxxxxxxx/cloud/TESTING/'
TESTING_API_IOT_APP_ID = secrets['appid']
TESTING_API_IOT_APP_KEY = secrets['appkey']