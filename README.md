
Развертывание сервиса и БД в Docker

1. Клонируйте проект
2. В корне проекта создайте файл .env, со следующим содержимым:
yandex_client_id='ваш client_id'
yandex_client_secret='ваш client_secret'
yandex_redirect_uri='https://oauth.yandex.ru/verification_code'
yandex_user_info='https://login.yandex.ru/info'
yandex_authorize='https://oauth.yandex.ru/authorize?response_type=code&client_id='
yandex_token='https://oauth.yandex.ru/token'

POSTGRES_DSN='postgresql+asyncpg://postgres:postgres@db:5432/test_db'

POSTGRES_DB=test_db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres

3. Для получения yandex_client_id, yandex_client_secret необходимо зарегистрировать 
приложение:
-https://yandex.ru/dev/id/doc/ru/register-client
-https://oauth.yandex.ru
В качестве Redirect URI для веб-сервисов указать: http://127.0.0.1:8008/token

4. В терминале перейти в корневую папку с проектом и ввести команду:
docker-compose up -d --build

5. После сборки проекта, в браузере перейти на: http://127.0.0.1:8008/docs
6. Для авторизации в приложении необходимо в другой вкладке браузера перейти 
по адресу: 127.0.0.1:8008/login_yandex
Произойдет переход на страницу авторизации через яндекс, где необходимо ввести логин и пароль
7. После этого API приложения станет доступен
