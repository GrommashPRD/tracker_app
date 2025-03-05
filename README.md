Проект для отслеживания url-адрессов.

Для того чтобы начать пользование используйте команды:
1) make start
2) make stop
3) make test
4) make migrate

DOCUMENTATION API - http://127.0.0.1:8000/swagger/?format=openapi

Для того чтобы начать пользоваться приложением вам нужно:
1) Зарегистрировать пользователя:
http://127.0.0.1:8000/api/auth/users/
```
curl --location 'http://127.0.0.1:8000/api/auth/users/' \

--header 'Cookie: csrftoken=cguiLxO9Tw1YJ1tBlIUy8sV7456hTkc' \

--form 'username="root"' \

--form 'password="root"'
```
2) Авторизоваться и получить access_token:
http://127.0.0.1:8000/auth/token/login/

```
curl --location 'http://127.0.0.1:8000/auth/token/login/' \

--header 'Cookie: csrftoken=cguiLxO9TwfglI56V7UdG7hTkc' \

--form 'username="root"' \

--form 'password="Tkbcttdrf"'
```
3) POST записей в базу данных:

#### _Важно в запросе использовать свой ACCESS_TOKEN_

http://127.0.0.1:8000/visited_links
```
curl --location 'http://127.0.0.1:8000/visited_links' \

--header 'Authorization: Token <YOUR_ACCESS_TOKEN>' \

--header 'X-User-ID: 2' \

--header 'Content-Type: application/json' \

--header 'Cookie: csrftoken=cguiLxO9TfgtBlIUy8sV7UdG7hTkc' \

--data '{

    "user_id": <ВАШ_USER_ID>,

    "urls": [

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
curl --location --request GET 'http://127.0.0.1:8000/visited_domains?start=1&end=9999999999' \

--header 'Authorization: Token bfa2b190d10f2473dfg139387379fccfdf3' \

--header 'X-User-ID: 2' \

--header 'Cookie: csrftoken=cguiLxO9Tw1YJ1tfgsV7UdG7hTkc' \

--form 'user_id="2"'
```

