"""
自定义线程，提取html文件中的id属性值
"""

import os
import re
import sys

sys.path.append('../Crawler/')
from Crawler.multithreading_crawler import TaskManager


class ExtractIdValue(TaskManager):
    """
    自定义多线程，提取html中标签的id属性值，并将属性值输出

    attributes:
        - file_dir: 存储html文件的文件夹路径
        - output_dir: 提取出来的id属性值的输出路径
        - file_list: 待提取的html文件的文件名列表

    example:
        extract_id_value = ExtractIdValue('dir of html file', 'output dir')
        extract_id_value.load_file()
        extract_id_value.run()
    """

    def __init__(self, file_dir, output_dir):
        """
        构造器

        :param file_dir: 存储html文件的文件夹路径
        :param output_dir: 提取出来的id属性值的输出路径
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
        else:
            return None

    def do_task(self, task):
        """
        定义线程执行任务时的具体操作

        读取task对应的文件，使用正则表达式扫描html全文内容，匹配标签的id属性值，将匹配结果输出

        :param task: 要处理的html文件名
        :return: None
        """
        pattern = re.compile(r'\s+id="(.*?)?"')
        html = None
        with open(self.file_dir + '/' + task, 'r', encoding='utf-8') as f:
            html = f.read()
        result = pattern.findall(html)
        if len(result) > 0:  # 如果匹配到注释，将注释输出
            # print(result)
            file_name, suffix_name = os.path.splitext(task)
            with open(self.output_dir + '/' + file_name + '.txt', 'w', encoding='utf-8') as f:
                for id_value in result:
                    f.write(id_value + '\n')

    def load_file(self):
        """
        根据构造器，读取待提取html文件名列表

        :return: None
        """
        self.file_list = os.listdir(self.file_dir)
