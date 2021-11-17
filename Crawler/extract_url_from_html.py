"""
This program crawls the page according to the given link file, extracts URLs from HTML and stores them locally.
Some hyperlinks may be incomplete, and the program will automatically complete the hyperlinks by domain name.
"""
import os

import requests
from bs4 import BeautifulSoup

import multithreading_crawler
import url_tools


class ExtractUrl(multithreading_crawler.TaskManager):

    def __init__(self, links_file: str, output_dir: str):
        super().__init__()
        self.links_file = links_file
        self.output_dir = output_dir
        self.links = []
        self.index = -1
        if not os.path.exists(output_dir):
            os.mkdir(output_dir)
        # 创建记录已完成任务的文件
        with open(self.output_dir + '/over.txt', 'a+', encoding='utf-8') as over_file:
            over_file.close()

    def obtain_links(self):
        # 默认读取txt文件
        with open(self.links_file, 'r', encoding='utf-8') as links_file:
            links = links_file.readlines()
            for link in links:
                self.links.append(link.strip('\n'))

    def acquire_task(self):
        if len(self.links) > 0:
            self.index += 1
            return self.links.pop(), self.index
        else:
            return None

    def do_task(self, task):
        link = task[0]
        index = task[1]
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/94.0.4606.81 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9'
        }
        try:
            response = None
            if 'http' not in link:
                response = requests.get('http://' + link, timeout=60, headers=headers, verify=False)
            else:
                response = requests.get(link, timeout=60, headers=headers, verify=False)
            if 200 <= response.status_code < 300:
                soup = BeautifulSoup(response.text, 'lxml')
                list_a_tag = soup.find_all('a')
                links_set = set()
                if len(list_a_tag) == 0:
                    print(link, 'don\'t have a tag!')
                else:
                    # 提取链接
                    domain_name = url_tools.extract_domain_name_from_url(link)
                    for a_tag in list_a_tag:
                        if a_tag.get('href') is not None:
                            links_set.add(url_tools.handle_url(domain_name, a_tag.get('href')))  # 有些链接需要进行补全操作
                    # 将提取的链接，写入文件
                    with open(self.output_dir + '/' + str(index) + '.txt', 'w', encoding='utf-8') as result_file:
                        for _link in links_set:
                            result_file.write(_link + '\n')
                print(link, '成功！')
            else:
                print(link, response.status_code, '失败！')
        except Exception as e:
            print(e)
            print(link, 'error!')
        finally:
            # 将结果写入文件
            self.thread_lock.acquire()
            with open(self.output_dir + '/over.txt', 'a+', encoding='utf-8') as over_file:
                over_file.write(str(index) + ',' + link + '\n')
            self.thread_lock.release()


if __name__ == '__main__':
    extract_url = ExtractUrl('./task-list.txt', '.')
    extract_url.obtain_links()
    extract_url.run()
