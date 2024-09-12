from lib_secrets_manager import *
secrets_manager = SecretsManager()
secrets = secrets_manager.getSecretValue('api_weather')
TESTING_API_WEATHER_URL = 'https://xxxxxxxxxxxxxxx/app/v2/weather/'
TESTING_API_WEATHER_APP_ID = secrets['appid']
TESTING_API_WEATHER_APP_KEY = secrets['appkey']