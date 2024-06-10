import requests
from bs4 import BeautifulSoup

testMode=1

def test():
    print("-------------------[test]-------------------")
    url="https://zhuanlan.zhihu.com/p/359919073"
    res = requests.get(url)
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text, 'lxml')
    print(soup.title.text)

def main():
    print("-------------------[main]-------------------")

if __name__ == '__main__':
    if testMode:
        test()
    else:
        main()