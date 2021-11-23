import sys

sys.path.append('../Crawler/')

from Crawler.extract_url_from_html import ExtractUrl

if __name__ == '__main__':
    # 第一步，实例化ExtractURL对象，传入任务列表文件路径，输出目录路径
    extract_url = ExtractUrl('./task-list.txt', '.')
    # 第二步，调用obtain_links，读取所有的链接
    extract_url.obtain_links()
    # 第三步，调用run方法，执行程序
    extract_url.run()
