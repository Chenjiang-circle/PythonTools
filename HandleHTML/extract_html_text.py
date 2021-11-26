"""
自定义线程，批量提取html文件中的文本
"""
import os
import sys

from bs4 import BeautifulSoup

sys.path.append('../Crawler/')
from Crawler.multithreading_crawler import TaskManager


def extract_content(html_file: str):
    """
    提取html中的内容
    :param html_file: 待提取html文件
    :return:
    """
    soup = BeautifulSoup(open(html_file, 'r', encoding='utf-8'), 'lxml')
    return soup.get_text()


class ExtractHtmlText(TaskManager):
    """
    自定义线程，批量提取html文件中text内容

    attributes:
        - file_dir: 存放待提取text的html文件的文件夹路径
        - output_dir: 提取到的text的输出路径
        - file_list: 待提取的html文件的文件名列表

    example:
        extract_html_text = ExtractHtmlText('file_dir', 'output_dir')
        extract_html_text.load_file()
        extract_html_text.run()
    """

    def __init__(self, file_dir: str, output_dir: str):
        """
        构造器

        :param file_dir: 存放待提取text的html文件的文件夹路径
        :param output_dir: 提取到的text的输出路径
        """
        super().__init__()
        self.file_dir = file_dir
        self.output_dir = output_dir
        self.file_list = []
        if not os.path.exists(self.output_dir):  # 自动创建输出路径
            os.mkdir(self.output_dir)

    def acquire_task(self):
        if len(self.file_list) > 0:
            return self.file_list.pop()
        return None

    def do_task(self, task):
        """
        线程执行任务时的具体操作

        读取html文件，获取text，将text输出

        :param task: 待提取text的html文件名
        :return: None
        """
        file_name, suffix_name = os.path.splitext(task)
        text = extract_content(self.file_dir + '/' + task)
        with open(self.output_dir + '/' + file_name + '.txt', 'w', encoding='utf-8') as f:
            f.write(text)

    def load_file(self):
        """
        根据构造器，读取待提取html文件名列表

        :return: None
        """
        self.file_list = os.listdir(self.file_dir)
