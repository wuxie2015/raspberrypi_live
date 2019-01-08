#! /usr/bin/python
# -*- coding:utf-8 -*-
import urllib.request as urst
import re
import os
from bs4 import BeautifulSoup as bs


def get_pic(keywords):
    opener = urst.build_opener()
    header = ("User-Agent","Mozilla/5.0(Macintosh;Intel Max OS X 10.13;rv55.0 Gecko/20100101 Firefox/55.0)")
    # baiduSearch = "http://image.baidu.com/search/index?tn=baiduimage&ipn=r&ct=201326592&cl=2&lm=-1&st=-1&fm=result&fr=&sf=1&fmq=1545808688070_R&pv=&ic=&nc=1&z=&hd=&latest=&copyright=&se=1&showtab=0&fb=0&width=&height=&face=0&istype=2&ie=utf-8&word={}"
    baidu_url = "http://image.baidu.com/search/index?tn=baiduimage&ipn=r&ct=201326592&cl=2&lm=-1&st=-1&fm=result&fr=&sf=1&fmq=1546591055545_R&pv=&ic=&nc=1&z=&hd=&latest=&copyright=&se=1&showtab=0&fb=0&width=&height=&face=0&istype=2&ie=utf-8&word=%E9%A9%AC%E8%B7%AF"
    opener.addheaders = [header]
    # keywords = keywords.replace('','+')
    # baidu_url = baiduSearch.format(keywords)
    data = opener.open(baidu_url).read()
    soup = bs(data,'lxml',from_encoding='utf-8')
    img_tags = soup.findAll('script', {'type': 'text/javascript'})
    links = []
    for chaos in img_tags:
        chaos_str = chaos.string
        # 有的内容是 None，在判断式那边会报错，因此直接加上 try 来把这个问题避开，如果报错了，就 continue 即可
        try:
            if 'ObjURL' in chaos_str:
                # 发现了‘ObjURL’ 后面的网址就是我们要的网址，因此用这个词把字符串分段组成新的 list
                Split = chaos_str.split('objURL":"')
                # 使用正则匹配后面我们期望看到的网址样貌，记得使用的是 ”懒惰模式“
                target_format = re.compile('^(http)s?.*?[^"]?.*?(jpg|png|jpeg|gif)')
                for chaos_split in Split:
                    # 同样为了达到避免报错的目的，而设置的 try / except
                    try:
                        # 把匹配成功的内容放到那个空的 list 里面
                        i = target_format.match(chaos_split).group()
                        links.append(i)
                    except:
                        continue
        except:
            continue
    return links

# 定义一个函数用来把上面形成 list 的图片网址集合下载下来，并根据其搜寻名称放置到我们喜欢的文件夹路径中
def save_images(links_list, keywords):
    # 由于在使用电脑呼叫文件的时候，不希望看到空格，因此这边使用 "_" 替代
    # folderName = keywords.replace(' ', '_')
    folderName = "picture"
    # 使用 join 好处是只要输入两个谁前谁后要排起来的路径名即可，不用中间还自己加 "/" 之类的东西
    directory = os.path.join(input('Enter the path to store the images: '), folderName)
    # 如果那个路径里面没有这个文件夹，那就创造一个，有的话就莫不作为
    if not os.path.isdir(directory):
        os.mkdir(directory)
        for sequence, link in enumerate(links_list):
            # 使用该图片网址在 list 中的排序来命名，并且重新生成一个最终的下载状态（包含档名）
            savepath = os.path.join(directory, '{:06}.png'.format(sequence))
            # 如果图片文件夹里面有一些隐藏文件，会导致下载失败，那就用 try 避开，让程序继续运行下去
            try:
                # 用这函数下载图片网址，并且把下载下来的东西放到指定的路径里面
                urst.urlretrieve(link, savepath)
            except:
                continue

# 如果呼叫的这些函数名字都是写在这个文档的函数，并非 import 进来的话，则运行；否则忽略
if __name__ == '__main__':
    keyword = 'road'
    # links_from_google = google_get_links(keyword)
    links_from_baidu = get_pic(keyword)
    save_images(links_from_baidu, keyword)




