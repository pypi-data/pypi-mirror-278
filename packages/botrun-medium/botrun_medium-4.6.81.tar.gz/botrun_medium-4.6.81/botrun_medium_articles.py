import os
import threading
from queue import Queue

import click
from dotenv import load_dotenv
from medium_api import Medium

import json

load_dotenv()

# 從環境變數中讀取 API Key
api_key = os.getenv('RAPIDAPI_KEY')

# 創建 Medium 物件
medium = Medium(api_key)

# 設定最大線程數
MAX_THREADS = 50


def fetch_article_data(article_id, results, titles):
    """抓取文章資料並存入結果列表"""
    try:
        article = medium.article(article_id=article_id)
        article_data = {
            'title': article.title,
            'subtitle': article.subtitle,
            'user_id': article.author.user_id,
            'topics': article.topics,
            'lang': article.lang,
            'last_modified_at': article.last_modified_at.isoformat(),
            'url': article.url,
            'content': article.content
        }
        results[article_id] = article_data
        titles[article_id] = article.title
    except Exception as e:
        results[article_id] = f"Error fetching article: {e}"


def worker(queue, results, titles):
    """線程 worker 函數，用於從隊列中取出文章 ID 並抓取資料"""
    while not queue.empty():
        article_id = queue.get()
        fetch_article_data(article_id, results, titles)
        queue.task_done()


def get_article_id_from_url(url):
    """從文章 URL 中解析出文章 ID"""
    return url.split('-')[-1]


@click.command()
@click.option('--input_file', default='json/articles_list.json', help='輸入 JSON 檔案名稱', show_default=True)
def botrun_medium_articles(input_file):
    # 確保輸出目錄存在
    output_dir = './json/articles/'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 從 JSON 檔案中讀取文章 ID 列表
    with open(input_file, 'r', encoding='utf-8') as file:
        articles = json.load(file)
        article_ids = [get_article_id_from_url(article['url']) for article in articles]

    # 使用 queue 來管理文章 ID
    queue = Queue()
    for article_id in article_ids:
        queue.put(article_id)

    # 存放文章內容的字典
    results = {}
    titles = {}

    # 創建和啟動線程
    threads = []
    for _ in range(min(MAX_THREADS, len(article_ids))):
        thread = threading.Thread(target=worker, args=(queue, results, titles))
        thread.start()
        threads.append(thread)

    # 等待所有線程完成工作
    for thread in threads:
        thread.join()

    # 輸出結果
    for article_id in results:
        filename = os.path.join(output_dir, f"{article_id}.json")
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(results[article_id], f, ensure_ascii=False, indent=4)
        print(f"已抓文章: {titles[article_id]}")


if __name__ == '__main__':
    botrun_medium_articles()  # 會解析命令列參數
