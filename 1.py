
hello world 
# 当当网图书, 使用正则表达式取出书籍标题，价格，图片路径：
#    http://category.dangdang.com/pg1-cp01.01.02.00.00.00.html

import re
import requests
import time
import threading

def dangdang(page=1):
    # 1. 爬取网页源码
    url = f'http://category.dangdang.com/pg{page}-cp01.01.02.00.00.00.html'
    res = requests.get(url)
    # print(res.text)
    # content = res.content.decode('gb2312')
    content = res.text

    # 2. 使用正则
    pattern2 = '<ul class="bigimg" id="component_59">(.*?)</ul>'
    content2 = re.findall(pattern2, content, re.S)[0]
    # print(content2)

    # 第1个图书
    pattern3 = "<img src='(.*?)' alt='(.*?)'.*?<span class=\"search_now_price\">(.*?)</span>"
    content3 = re.findall(pattern3, content2, re.S)
    # print(content3)
    # print(len(content3))

    # 第2-60个图书
    pattern4 = "<img data-original='(.*?)'.*?alt='(.*?)'.*?<span class=\"search_now_price\">(.*?)</span>"
    content4 = re.findall(pattern4, content2, re.S)
    # print(content4)
    # print(len(content4))

    # 3. 打印内容
    book_list = content3 + content4

    # 书籍存入本地
    fp = open('dangdang.txt', 'a', encoding='utf-8')
    for book in book_list:
        # print(book[1], book[0], book[2])
        fp.write(str(page) + '-' + str((book[1], book[0], book[2])) + '\n')
        fp.flush()  # 刷新缓冲区

    fp.close()


if __name__ == '__main__':
    start = time.time()

    t_list = []
    for i in range(1, 21):
        dangdang(i)  # 同步: 耗时:12s

        # 异步: 耗时1.8s
        # t = threading.Thread(target=dangdang, args=(i,))
        # t.start()
        # t_list.append(t)

    for t in t_list:
        t.join()

    end = time.time()
    print('耗时:', end - start)


