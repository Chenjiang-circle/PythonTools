"""
This program crawls the page according to the given link file, extracts URLs from HTML and stores them locally.
Some hyperlinks may be incomplete, and the program will automatically complete the hyperlinks by domain name.
"""
import os

import requests
from bs4 import BeautifulSoup

from multithreading_crawler import TaskManager
import url_tools


class ExtractUrl(TaskManager):
    """多线程爬取网页并提取其中的超链接

    ExtractUrl类继承了TaskManager类，并实现了acquire_task和do_task方法。
    使用该类进行提取网页超链接时，只需要在实例化时传入“links_file”和“output_dir”两个参数。按顺序分别调用obtain_links方法和run方法，
    便可启动程序，输入要创建的线程数，程序便会根据links_file中的链接，为线程分配任务。

    example:

    extract_url = ExtractUrl('./list.txt', '.')

    extract_url.obtain_links()

    extract_url.run()

    Attributes:
        links_file: 存储所有要爬取的页面对应的链接的文件路径
        links_file: 存储所有要爬取的页面对应的链接的文件路径
        output_dir: 提取出来的超链接的输出路径
        links: 所有要爬取的页面对应的链接列表
        task_id: 每个线程分配到的任务编号
    """

    def __init__(self, links_file: str, output_dir: str):
        """构造函数

        :param links_file: 存储所有要爬取的页面对应的链接的文件路径
        :param output_dir: 提取出来的超链接的输出路径
        """
        super().__init__()
        self.links_file = links_file
        self.output_dir = output_dir
        self.links = []
        self.task_id = -1
        if not os.path.exists(output_dir):  # 如果输出文件夹不存在，就创建
            os.mkdir(output_dir)
        # 创建记录已完成任务的文件
        with open(self.output_dir + '/over.txt', 'a+', encoding='utf-8') as over_file:
            over_file.close()

    def obtain_links(self):
        """读取存储链接的文件，将链接存储到links列表中

        :raises FileNotFoundError: 类实例化时传递的参数links_file对应的文件不存在
        """
        # 默认读取txt文件
        with open(self.links_file, 'r', encoding='utf-8') as links_file:
            links = links_file.readlines()
            for link in links:
                self.links.append(link.strip('\n'))

    def acquire_task(self):
        """线程获取任务的方法

        线程在获得锁之后，执行该方法。在执行完该方法之后，对应的线程会释放对应的锁。

        :return:
            如果还有链接没有被分配给线程，返回一个Tuple类型数据，其中第一个元素为表示链接的str类型数据，
            第二个元组为表示该线程的任务id的int类型数据。如果没有剩余链接可以分配，返回None
        """
        if len(self.links) > 0:
            self.task_id += 1
            return self.links.pop(), self.task_id
        else:
            return None

    def do_task(self, task):
        """每个线程执行的任务

        线程根据分配到的任务，使用requests库爬取相应链接的页面，之后使用BeautifulSoup解析HTML，获取页面中的超链接，
        并根据指定的输出目录，将超链接写入文件中。

        :param task: Tuple类型，线程要执行的任务信息，包括要爬取的链接、任务id
        :return: None
        """
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
            # 将完成的任务url和id写入文件
            self.thread_lock.acquire()
            with open(self.output_dir + '/over.txt', 'a+', encoding='utf-8') as over_file:
                over_file.write(str(index) + ',' + link + '\n')
            self.thread_lock.release()


if __name__ == '__main__':
    extract_url = ExtractUrl('../Example/task-list.txt', '.')
    extract_url.obtain_links()
    extract_url.run()
