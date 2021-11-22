"""
单线程或多线程提取HTML页面中的js链接
"""
import os
import sys

from bs4 import BeautifulSoup

sys.path.append('../Crawler/')
from Crawler.multithreading_crawler import TaskManager


class ExtractJsLink(TaskManager):
    """
    单线程或多线程批量处理HTML页面中的js链接，并将链接输出到指定目录下

    使用实例：
    extract_js_link = ExtractJsLink('.', '.')  # 提取当前文件夹里面的html中的js链接，并输出到当前文件夹下
    extract_js_link.load_files()
    extract_js_link.run()
    """

    def __init__(self, html_file_dir: str, output_dir: str):
        """
        ExtractJsLink构造函数

        :param html_file_dir: 要处理的html文件所在文件夹
        :param output_dir: 处理结果的输出路径
        """
        super().__init__()
        self.html_file_dir = html_file_dir
        self.html_file_list = []
        self.output_dir = output_dir
        self.hand_out_tasks = []
        # 如果输出目录不存在，就创建它
        if not os.path.exists(output_dir):
            os.mkdir(output_dir)

    def load_files(self):
        """
        从指定的文件夹中去除html文件列表

        :return: None
        :raises 文件夹不存在: 该类在实例化时所指定的文佳夹不存在
        """
        self.html_file_list = os.listdir(self.html_file_dir)

    def acquire_task(self):
        """
        给多线程分发任务。从读取的文件列表中查抄未被处理且未配分配的文件，把文件名返回。

        :return: 如果还有没有处理的任务，就将要处理的html文件名返回；否则，返回None
        """
        while len(self.html_file_list) > 0:
            file_name = self.html_file_list.pop()
            prefix_name, suffix_name = os.path.splitext(file_name)
            if suffix_name != '.html':  # 如果不是html不处理
                print(suffix_name, '不是html')
                continue
            # 如果该任务还没有分发出去，并且该任务之前也没有完成，就将任务分配出去
            if file_name not in self.hand_out_tasks and not os.path.exists(self.output_dir + '/' + prefix_name + '.txt'):
                self.hand_out_tasks.append(file_name)
                return file_name
        return None

    def do_task(self, task):
        """
        每个线程要做的任务。具体步骤如下：

        - 首先使用BeautifulSoup解析HTML文件
        - 提取所有<script>标签中src属性值
        - 提取所有<link>标签中type类型为text/javascript，href属性中的值
        - 提取所有的<a>标签中的href属性值
        - 提取<td>标签中的内容（如果<td>没有嵌套其他标签）
        - 提取<span>标签中的内容
        - 对上述提取出来的字符串，使用正则表达式匹配js链接，并将储存的结果输出

        :param task: 待处理文件名
        :return: None
        """
        contents = []
        soup = BeautifulSoup(open(self.html_file_dir + '/' + task, 'rb'), 'lxml')
        a_tags = soup.findAll('a')
        if len(a_tags) > 1:
            for a_tag in a_tags:
                if a_tag.get('href'):
                    contents.append(a_tag.get('href'))
        script_tags = soup.findAll('script')
        if len(script_tags) > 1:
            for script_tag in script_tags:
                if script_tag.get('src'):
                    contents.append(script_tag.get('src'))
        link_tags = soup.findAll('link')
        if len(link_tags) > 1:
            for link_tag in link_tags:
                if link_tag.get('type') == 'text/javascript':
                    if link_tag.get('href'):
                        contents.append(link_tag.get('href'))
        # span_tags = soup.findAll('span')
        # for span_tag in span_tags:
        #     contents.append(span_tag.contents)
        # td_tags = soup.findAll('td')
        # for td_tag in td_tags:
        #     if td_tag.string:
        #         contents.append(td_tag.string)

        prefix_name, suffix_name = os.path.splitext(task)
        if len(contents) < 1:
            return
        with open(self.output_dir + '/' + prefix_name + '.txt', 'a+', encoding='utf-8') as f:
            for content in contents:
                try:
                    if '.js' in content:
                        f.write(content + '\n')
                except Exception as e:
                    print(e)
                    print(content, contents)

