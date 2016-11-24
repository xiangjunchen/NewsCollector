#coding:utf-8  
import urllib  
import re  
import json  
#用户id+评论+顶  
def getHtml(url):  
    page=urllib.urlopen(url)  
    html=page.read()  
    return html  
def getItems(html):  
    #一开始写的时候还在该函数的开始加了这两句代码，主要就是这两个方法没有了解清楚  
    #data1=json.dumps(html)  
    #data=json.loads(data1)  
    #这是没必要的，直接替换再转换就可以。将开头的var replyData=和结尾的;替换掉再转成Python时才能对字典进行处理  
    reg=re.compile(" \[<a href=''>")  
    data=reg.sub(' ',html)  
    reg1=re.compile("var replyData=")  
    data=reg1.sub(' ',data)  
    reg2=re.compile('<\\\/a>\]')  
    data=reg2.sub('',data)  
    reg3=re.compile(';')  
    data=reg3.sub('',data)  
    reg4=re.compile('<span(.*?)/span>')#<span>(.*?)</span>这样匹配是不对的,替换不掉（还不清楚原因）  
    data=reg4.sub('',data)  
    reg5=re.compile('')  
    data=reg5.sub('',data)  
    data=json.loads(data)#这句代码的作用是将数据转换成Python对象，然后根据字典的key取值得到想要的内容  
    f=open('wy.txt','a+')  
    for i in data['hotPosts']:  
        f.write(i['1']['f'].encode('utf-8')+'\n')  
        f.write(i['1']['b'].encode('utf-8')+'\n')  
        f.write(i['1']['v'].encode('utf-8')+'\n')  
    f.close()  
  
url='http://comment.news.163.com/data/news_guonei8_bbs/df/B9C8EJDC0001124J_1.html'#（热门跟帖）  
html=getHtml(url)  
getItems(html) 

#http://news.163.com/16/1124/13/C6L2K0IP000187VE.html

#"productKey" : a2869674571f77b5a0867c3d71db5856

#http://comment.news.163.com/api/v1/products/a2869674571f77b5a0867c3d71db5856/threads/C6L2K0IP000187VE

#"boardId": news2_bbs

#http://comment.news.163.com/news2_bbs/C6L2K0IP000187VE.html

#http://comment.news.163.com/api/v1/products/a2869674571f77b5a0867c3d71db5856/threads/C6L2K0IP000187VE/comments/newList?offset=0&limit=30
