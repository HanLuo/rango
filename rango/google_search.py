import json
import urllib.parse
import urllib.request


def read_google_key():
    google_search_key = None

    try:
        with open('search.txt', 'r') as f:
            google_search_key = f.readlines().strip()
    except:
        raise IOError('search.key file not found!')

    return google_search_key

def run_query(search_terms, size=10):
    google_key = read_google_key()

    if not google_key:
        raise IOError('google_key not found!')
    root_url = 'https:// cse.google.com/cse'

    # 处理查询的字符串
    query_string = urllib.parse.quote(search_terms)

    search_url = ('{root_url}?cx={cx}&q={query}').format(root_url = root_url, cx=google_key, query=query_string)
    print (search_url)

    results = []
    try:
        response = urllib.request.urlopen(search_url).read().decode('utf-8')
        json_response = json.loads(response)
        print (json_response)
    except:
        pass

if __name__ == "__main__":
    run_query('django')
