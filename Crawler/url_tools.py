

def extract_domain_name_from_url(url: str):
    """
    从url中取出域名
    """
    if 'http' not in url:
        url = 'http://' + url
    link_split = url.split('/')
    domain = ''
    for i in range(len(link_split)):
        if 'http' in link_split[i]:
            j = i+1
            while link_split[j] == '':
                j += 1
            domain = link_split[j]
            break
    return domain


def handle_url(domain, url):
    """
    补全某些链接
    """
    if len(url) == 0 or 'javascript' in url:
        return url
    if url == '#' or url == '###':
        return url
    if url[0:2] == '//':
        return 'http:' + url
    if 'http' not in url:
        final_url = 'http://' + domain + '/' + url
        return final_url
    else:
        return url


if __name__ == '__main__':
    # test/测试
    print(extract_domain_name_from_url('//www.baidu.com/index.html'))
