"""
自定义线程，自定义提取标签属性，将指定的属性值输出到给定文件夹下
"""

import os
import re
import sys

from typing import List

sys.path.append('../Crawler/')
from Crawler.multithreading_crawler import TaskManager


class ExtractAttributesValues(TaskManager):
    """
    自定义多线程，在html文件中将指定属性列表的属性值提取出来，并分类输出到指定文件夹中

    attributes:
        - file_dir: 存储待处理的html的文件夹路径
        - output_dir: 处理结果的输出路径
        - attributes: 要提取的属性值对应的属性列表
        - file_list: 待处理的html文件名列表

    examples:
        extract_attributes_values = ExtractAttributesValues('the path of file dir', 'the path of output dir', ['id', 'class'])
        extract_attributes_values.load_file()
        extract_attributes_values.run()
    """

    def __init__(self, file_dir: str, output_dir: str, attributes: List[str]):
        """
        构造器

        如果输出路径不存在，自动创建输出路径

        :param file_dir: 存储待处理的html的文件夹路径
        :param output_dir: 处理结果的输出路径
        :param attributes: 要提取的属性值对应的属性列表
        """
        super().__init__()
        self.file_dir = file_dir
        self.output_dir = output_dir
        self.attributes = attributes
        self.file_list = []
        if not os.path.exists(self.output_dir):  # 如果输出路径不存在，就创建该文件夹
            os.mkdir(self.output_dir)

    def acquire_task(self):
        if len(self.file_list) > 0:
            return self.file_list.pop()
        else:
            return None

    def do_task(self, task):
        """
        线程执行任务时的具体操作

        线程根据task，读取相应的html文件，按照self.attributes中的属性列表，使用正则表达将它们一一取出，并将结果输出到指定目录下

        :param task: 待执行的html文件名
        :return: None
        """
        if len(self.attributes) < 1:
            print('待提取属性为空！')
            return
        for attribute in self.attributes:
            pattern_str = r'\s+' + attribute + '="(.*?)?"'
            pattern = re.compile(pattern_str)
            html = None
            with open(self.file_dir + '/' + task, 'r', encoding='utf-8') as f:
                html = f.read()
            result = pattern.findall(html)
            if len(result) > 0:  # 如果匹配到注释，将注释输出
                # print(result)
                if not os.path.exists(self.output_dir + '/' + attribute):
                    os.mkdir(self.output_dir + '/' + attribute)
                file_name, suffix_name = os.path.splitext(task)
                with open(self.output_dir + '/' + attribute + '/' + file_name + '_' + attribute + '.txt', 'w', encoding='utf-8') as f:
                    for id_value in result:
                        f.write(id_value + '\n')

    def load_file(self):
        """
        根据构造器，读取待提取html文件名列表

        :return: None
        """
        self.file_list = os.listdir(self.file_dir)
