"# tracker_app" 

Проект для отслеживания url-адрессов.

Для того чтобы начать пользование используйте команды:
1) make start
2) make stop

Для тестирования функционала можно использовать команды: 

Чтобы создать запись о пользователе:

curl --location 'http://127.0.0.1:8000/visited_links' \
--header 'X-User-Id: 1' \
--header 'Content-Type: application/json' \
--data '{

   "urls": [
      "https://ya.ru/",
      "https://ya.ru/search/?text=мемы+с+котиками",
      "https://sber.ru",
      "https://stackoverflow.com/questions/65724760/how-it-is"
       ]	
}

Для получения информации по посещенным пользователем ссылкам:

curl --location 'http://127.0.0.1:8000/visited_domains?start=1&end=1798938075' \
--header 'X-User-Id: 1'
