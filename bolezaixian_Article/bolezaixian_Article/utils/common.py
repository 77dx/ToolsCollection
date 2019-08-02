#-*-coding:utf-8-*-

import hashlib
import re

def get_md5(url):
    if isinstance(url,str):
        url = url.encode("utf-8")

    m = hashlib.md5()
    m.update(url)
    return m.hexdigest()


def extract_num(value):
    if re.match(".*?(\d+).*", value):
        nums = int(re.match(".*?(\d+).*", value).group(1))
    else:
        nums = 0
    return nums




if __name__ == '__main__':
    print(get_md5("http://www.baidu.com".encode("utf-8")))