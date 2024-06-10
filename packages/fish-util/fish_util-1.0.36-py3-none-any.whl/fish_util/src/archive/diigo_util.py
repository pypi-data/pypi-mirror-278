from pydiigo import DiigoApi

# Initialize API
DIIGO_USERNAME="yutianran666@gmail.com"
DIIGO_PASSWORD="Ytr@0113#diigo"
API_KEY="24f624a4c85cabc6"

api = DiigoApi(user=DIIGO_USERNAME, password=DIIGO_PASSWORD, apikey=API_KEY)

# set test mode
testMode=1

def main():
    print("-------------------[main]-------------------")

def test():
    print("-------------------[test]-------------------")
    url='https://juejin.cn/post/6844903869424599053'
    title='VSCode 利用 Snippets 设置超实用的代码块'
    addBookmark(title,url)

def addBookmark(title,url):
    print("-------------------[addBookmark]-------------------")
    mTitle=title+"-AddByPython"
    result = api.bookmark_add(title=mTitle, url=url,description='',shared='no', tags='')
    print(result['message'])

def searchBookmark():
    print("-------------------[searchBookmark]-------------------")
    bookmarks = api.bookmarks_find(users='DIIGO_USER_NAME')
    for bookmark in bookmarks:
      print(bookmark.title)
      print(bookmark.url)
      print(bookmark.tags)
      print(bookmark.desc)
      print('-' * 10)

if __name__ == '__main__':
    if testMode:
        test()
    else:
        main()