## ТЗ
Протестировать сервис (проверить наличие багов, написать тесты)

## News parser
1. API, которое получает новости за заданный период из базы
2. Парсер, который каждые 10 минут получает новости
с сайта http://mosday.ru/news/tags.php?metro

Метод GET:
/metro/news?day=5

В качестве ответа возвращает JSON новости, которые опубликованы за последние 5 дней (включительно)
1. заголовок
2. url картинки
3. дата публикации

```
{
    "article_title": "example",
    "image_url": "http://localhost/news1234",
    "published_date": "06.01.2023 10:30"
}
```


### Инструкция запуска
1. Задать значение PARSE_DELAY в файле `.env`
2. Выполнить команду `docker-compose up -d --build`
3. Открыть с нужным параметром `day` ссылку `http://0.0.0.0:11050/metro/news?day=3`
