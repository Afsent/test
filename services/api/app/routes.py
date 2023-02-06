from flask import request, jsonify
from psycopg2.extras import NamedTupleCursor

from app import app

from lib.db import Pool


@app.route("/metro/news", methods=['GET'])
def news():
    date_range = request.args.get("day", 1)
    articles = get_articles(date_range)
    response = [
        {
            "article_title": article.title,
            "image_url": article.image_url,
            "published_date": article.published_date.strftime("%d.%m.%Y %H:%M")
        }
        for article in articles
    ]
    return jsonify(response)


def get_articles(date_range):
    print(date_range)
    query = """
        SELECT title, image_url, published_date
        FROM article
        WHERE published_date >= CURRENT_DATE - %(date_range)s::interval
    """
    with Pool.get_db() as db:
        cursor = db.cursor(cursor_factory=NamedTupleCursor)
        cursor.execute(query, {"date_range": f"{date_range} DAYS"})
        return cursor.fetchall()
