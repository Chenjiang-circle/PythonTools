"""
单线程或多线程提取html中的注释内容
"""
import os
import re
import sys

sys.path.append('../Crawler/')
from Crawler.multithreading_crawler import TaskManager


class ExtractAnnotation(TaskManager):
    """
    自定义线程提取指定html文件中的注释，并将注释输出到指定文件夹下

    attribute:
        - file_dir: 存放待提取注释的html文件的文件夹路径
        - output_dir: 提取到的注释的输出路径
        - file_list: 待提取的html文件的文件名列表

    example:
        extract_annotation = ExtractAnnotation('dir of html file', 'output dir')
        extract_annotation.load_file()
        extract_annotation.run()
    """

    def __init__(self, file_dir, output_dir):
        """
        构造器

        :param file_dir: 存放待提取注释的html文件的文件夹路径
        :param output_dir: 提取到的注释的输出路径
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
        每个线程执行任务的具体操作。

        每个线程在获取到任务之后，根据任务找到相应的文件，并打开，使用正则表达式对全文进行匹配，输出匹配到的内容。

        :param task: 要执行的某个html文件名
        :return: 如果待提取的html文件中包含注释，将提取到的注释输出到指定文件夹下；反之，什么也不做。
        """
        pattern = re.compile(r'<!--(.*?|\n*?)?-->')
        html = None
        with open(self.file_dir + '/' + task, 'r', encoding='utf-8') as f:
            html = f.read()
        result = pattern.findall(html)
        if len(result) > 0:  # 如果匹配到注释，将注释输出
            file_name, suffix_name = os.path.splitext(task)
            with open(self.output_dir + '/' + file_name + '.txt', 'w', encoding='utf-8') as f:
                for annotation in result:
                    f.write(annotation.strip('\n') + '\n')

    def load_file(self):
        """
        根据构造器，读取待提取html文件名列表

        :return: None
        """
        self.file_list = os.listdir(self.file_dir)
