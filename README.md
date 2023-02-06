## ТЗ
Протестировать сервис (проверить наличие багов, написать тесты)

## News parser
1. API, которое получает новости за заданный период из базы
2. Парсер, который каждые 10 минут парсит новости
с сайта http://mosday.ru/news/tags.php?metro
(достаточно будет просто взять те новости, что есть
при первой загрузке)
и сохраняет в базу с меткой когда эти новости были получены.

Пример метода
/metro/news?day=5

В качестве ответа вернуть JSON новости которые о
публикованы за последний 5 дней (включительно)

1. заголовок
2. url картинки
3. дата публикации (YYYY-mm-dd)


### USAGE
1. Set PARSE_DELAY in `.env`
2. Create some local directory for postgres data and set DATA_POSTGRES_DIR in `.env`
3. Run `docker-compose up -d --build`
4. Open with needed `day` param `http://0.0.0.0:11050/metro/news?day=3`
