import requests
from django.core.management.base import BaseCommand

YANDEX_CLIENT_ID = '86b79240340b423b928af836b1ca7bea'
YANDEX_CLIENT_SECRET = '983c592cefe1464e8f3b4fe1345b5233'
REDIRECT_URI = 'https://webhook.site/f37b99b3-4f8d-4e30-8d85-cbea879b3bc3'

def get_access_token(auth_code):
    token_url = "https://oauth.yandex.ru/token"
    data = {
        'grant_type': 'authorization_code',
        'code': auth_code,
        'client_id': YANDEX_CLIENT_ID,
        'client_secret': YANDEX_CLIENT_SECRET,
        'redirect_uri': REDIRECT_URI
    }

    response = requests.post(token_url, data=data)
    if response.status_code == 200:
        return response.json().get('access_token')
    return None

class Command(BaseCommand):
    help = 'Получение токена доступа Yandex Music'

    def handle(self, *args, **kwargs):
        print("Перейдите по следующей ссылке для авторизации:")
        print(f"https://oauth.yandex.ru/authorize?response_type=code&client_id={YANDEX_CLIENT_ID}&redirect_uri={REDIRECT_URI}")

        auth_code = input("Введите код авторизации: ")
        access_token = get_access_token(auth_code)
        if access_token:
            self.stdout.write(self.style.SUCCESS(f'Ваш токен доступа: {access_token}'))
        else:
            self.stdout.write(self.style.ERROR("Не удалось получить токен доступа."))
