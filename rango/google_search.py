import json
import urllib.parse
import urllib.request
import os
import socket

# Google Customer Search API
# 参考 https://blog.csdn.net/yjn03151111/article/details/41492461

def read_google_key():
    google_search_key = None
    google_api_key = None

    # 获得当前目录
    # path = os.getcwd()
    path = os.path.abspath(os.path.dirname(__file__))
    print(path)

    url = ('{path}//..//key//{name}').format(path=path, name='search.key')
    try:
        with open(url, 'r') as f:
            google_search_key = f.readline().strip()
    except:
        raise IOError('search.key file not found!')

    url = ('{path}//..//key//{name}').format(path=path, name='api.key')
    try:
        with open(url, 'r') as f:
            google_api_key = f.readline().strip()
    except:
        raise IOError('api.key file not found!')

    return google_search_key, google_api_key


def run_query(search_terms, size=10):
    google_key = read_google_key()
    if not google_key:
        raise IOError('google_key not found!')
    root_url = 'https://www.googleapis.com/customsearch/v1'

    # 处理查询的字符串
    query_string = urllib.parse.quote(search_terms)

    search_url = ('{root_url}?key={key}&cx={cx}&q={q}').format(
        root_url=root_url, key=google_key[1], cx=google_key[0], q=query_string)
    print(search_url)

    # 因不可抗力因素，要使用代理
    # timeout = 2
    # socket.setdefaulttimeout(timeout)
    # proxy_support = urllib.request.ProxyHandler(
    #     {"http": "127.0.0.1:8080"})
    # opener = urllib.request.build_opener(proxy_support)
    # urllib.request.install_opener(opener)
    response = urllib.request.urlopen(search_url).read().decode('utf-8')
    json_response = json.loads(response)
    # path = os.path.abspath(os.path.dirname(__file__))
    # f = open('{path}//1.txt'.format(path=path), 'w')
    # repal = response.replace(u'\xa0', u'')
    # f.write(repal)
    # f.close()
    result = []
    for item in json_response['items']:
        result.append({'title': item['title'], 'link': item['link']})
    return result


if __name__ == "__main__":
    run_query('django')
