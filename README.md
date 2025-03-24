Проект для отслеживания url-адрессов.

Для того чтобы начать пользование используйте команды:
1) make start
2) make stop
3) make test
4) make migrate

METRICS - http://127.0.0.1:8000/metrics

DOCUMENTATION API - http://127.0.0.1:8000/swagger/?format=openapi

Для того чтобы начать пользоваться приложением вам нужно:
1) Зарегистрировать пользователя по методу POST:
http://127.0.0.1:8000/api/auth/users/

`{
    "username": "example",
    "password": "example"
}`

2) Авторизоваться и получить access_token по методу POST:
http://127.0.0.1:8000/auth/token/login/

**_REQUEST:_**

`{
    "username": "example",
    "password": "example"
}`

_**RESPONSE:**_

`{
    "auth_token": "776fdfkg3dgb5dfh75e59b6af6bb6e58fb724162"
}`

3) POST записей в базу данных:

#### _Важно в запросе использовать свой ACCESS_TOKEN_

http://127.0.0.1:8000/visited_links
```
curl --location 'http://127.0.0.1:8000/visited_links' \
--header 'Authorization: Token <ВАШ auth_token ИЗ ШАГА 2>' \
--header 'Content-Type: application/json' \
--header 'Cookie: csrftoken=cguiLxO9Tw1YJ1tBlIUy8sV7UdG7hTkc' \
--data '{
    "user_id": 1,
    "urls": [
      "https://ya.ru/",
      "https://ya.ru/search/?text=мемы+с+котиками",
      "https://paspdf.ru",
      "https://stackoverflow.com/questions/65724760/how-it-is"
    ]
}'

```
4) GET на получение посещенных URL-адресов.

#### _ОБЯЗАТЕЛЬНЫЕ ПАРАМЕТРЫ end и start_

http://127.0.0.1:8000/visited_domains?start=1&end=9999999999
```
curl --location --request GET 'http://127.0.0.1:8000/visited_domains?start=1&end=9999999999' \
--header 'Authorization: Token <ВАШ auth_token ИЗ ШАГА 2>' \
--header 'Content-Type: application/json' \
--header 'Cookie: csrftoken=cguiLxO9Tw1YJ1tBlIUy8sV7UdG7hTkc' \
--data '{
    "user_id": 1
}'
```

