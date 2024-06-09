import os
from datetime import datetime

import click
from dotenv import load_dotenv
from medium_api import Medium

import json

load_dotenv()


def datetime_to_str(dt):
    if isinstance(dt, datetime):
        return dt.isoformat()
    raise TypeError(f"Object of type {type(dt)} is not JSON serializable")


def fetch_articles_to_file(username, output_file):
    rapidapi_key = os.getenv('RAPIDAPI_KEY')
    medium = Medium(rapidapi_key)
    user = medium.user(username=username)
    print("user:", user)
    user.fetch_articles()
    articles_data = []
    for article in user.articles:
        article_info = {
            'title': article.title,
            'subtitle': article.subtitle,
            'user_id': article.author.user_id,
            'topics': article.topics,
            'lang': article.lang,
            'last_modified_at': article.last_modified_at.isoformat(),
            'url': article.url
        }
        articles_data.append(article_info)
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(articles_data, f, ensure_ascii=False, indent=4, default=datetime_to_str)


@click.command()
@click.option('--username', default='bohachu', help='Medium 使用者名稱', show_default=True)
@click.option('--output_file', default='json/articles_list.json', help='輸出檔案名稱', show_default=True)
def botrun_medium_list(username, output_file):
    fetch_articles_to_file(username, output_file)


if __name__ == '__main__':
    botrun_medium_list()  # 會解析命令列參數