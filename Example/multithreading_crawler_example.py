"""
this is a demo about how to use the multithreading_crawler.py
Note:
You should create a class inheriting from TaskManager and implementing all abstract methods
including acquire_task method and do_task method. And then, you just need using run()
method to start your program.
"""

import requests

import sys

sys.path.append('../Crawler/')

from Crawler.multithreading_crawler import TaskManager

tasks = []

with open('./task-list.txt', 'r', encoding='utf-8') as f:
    lines = f.readlines()
    for line in lines:
        tasks.append(line.strip('\n'))


class MyCrawler(TaskManager):

    def acquire_task(self):
        if len(tasks) > 0:
            return tasks.pop()
        else:
            return None

    def do_task(self, task):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/94.0.4606.81 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9'
        }
        try:
            response = requests.get(task, timeout=60, headers=headers, verify=False)
            if 200 <= response.status_code < 300:
                return True
            else:
                return False
        except Exception as e:
            return False


if __name__ == '__main__':
    crawler = MyCrawler()
    crawler.run()
