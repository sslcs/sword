from bs4 import BeautifulSoup
import requests
import datetime
import time
import sys
import random
import win32api,win32con
import json

FILE_LAST = 'sword.txt'
URL = "http://book.zongheng.com/book/672340.html"
forum = "http://forum.zongheng.com/api/forums/postlist?bookId=672340"
last = ''

def get_header() :
    heads = {}
    heads['User-Agent'] = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1"
    return heads
    
def read_last() :
    # 读取上次保存的标题
    with open(FILE_LAST, 'a+') as file :
        file.seek(0)
        return file.read()

def write_last(title) :
    # 保存最新章节标题
    with open(FILE_LAST, 'w') as file :
        file.write(title)
        print('write : ' + title)
        
def get_least() :
    heads = get_header()
    html = requests.get(URL, headers=heads)
    soup = BeautifulSoup(html.content, "html.parser")
    least = soup.find(class_ = 'book-new-chapter')
    if not least :
        # 未能获得最新章节，脚本可能出错。
        # 1、查询过多需要输入验证码
        # 2、网络错误
        # 3、其他
        print("least: ", html.content)
        # 退出脚本，停止自动检查
        sys.exit()
    return least.find(class_ = 'tit').text

def check_time() :
    time_formatter = '%Y-%m-%d %H:%M:%S'
    time_str = datetime.datetime.now().strftime(time_formatter)
    print('Checked @ %s' % (time_str), flush = True)

def tip(title) :
    # 打印最新章节标题或请假内容。
    print(" new : ", title)
    
    # 弹出提醒对话框提示更新。
    # 可根据需要自行更改。
    # 标题： "提醒"
    # 内容： "好好工作！"
    win32api.MessageBox(None, "好好工作！", "提醒", win32con.MB_ICONASTERISK)
    
    # 退出脚本，停止自动检查
    sys.exit()
    
def ask_leave() :
    heads = get_header()
    data_reponse = requests.get(forum, headers=heads)
    data_str = data_reponse.content
    data_json = json.loads(data_str)
    tops = data_json['data']['topThread']
    for top in tops :
        title = top['title']
        if not title :
            title = top['content']
        # 论坛置顶的帖子标题包含‘请假’、‘么么哒’，视为请假！
        if title.find('请假') > 0 or title.find('么么哒') > 0 :
            return title

def check() :
    # 获取最新章节的标题
    least = get_least()  
    if least == last :
        # 最新章节和已保存相同，说明没有更新。
        # 检查有没有请假。
        leave = ask_leave()
        if leave :
            # 请假内容不为空，说明又请假！
            tip(leave)
        else :
            # 没有请假，打印检查时间。
            check_time()
    else :
        # 保存最新章节标题
        write_last(least)
        if last :
            # 如果上次保存章节不为空，说明有更新。
            # 提示已更新！
            tip(least)

if __name__ == '__main__' :
    # 从文件‘剑来.txt’中读取上一章标题
    last = read_last()
    print("last : ", last)
    
    # 随机120~180秒(2~3分钟)检查一下更新,太频繁有可能触发验证码
    while True :
        check()
        s = 60*2 + 60 * random.random()
        time.sleep(s)
