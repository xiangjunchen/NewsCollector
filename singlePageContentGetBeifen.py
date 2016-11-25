#coding:utf-8  
import urllib2
import json
import re

def GetPinglun(url):
    #http://news.163.com/16/0808/14/BTV3ABLP00014AEE.html
    pinglunshu=0    
    uid = url.split('.html')[0].split('/')[-1]
    comment_url = 'http://comment.news.163.com/api/v1/products/a2869674571f77b5a0867c3d71db5856/threads/%s'%uid
    response = urllib2.urlopen(comment_url)        
    html = response.read()
    data =json.loads(html)
    if data["tcount"]!=0:
        pinglunshu =  data["tcount"]
        uid =data["docId"]
        group = data["boardId"]
        comment_url = 'http://comment.news.163.com/%s/%s.html'%group%uid
        # print comment_url
        #self.queue_pinglun.put(comment_url+'@@@@@@'+url)
    return pinglunshu

GetPinglun('http://news.163.com/16/1124/13/C6L2K0IP000187VE.html')

#response = urllib2.urlopen('http://comment.news.163.com/api/v1/products/a2869674571f77b5a0867c3d71db5856/threads/C6L2K0IP000187VE')
#html = response.read()
##<title>国家食药监总局:对北京等12个省市开展水产品检查_网易新闻</title>
##<div class="post_time_source"> 

#foundTitle = re.search('<title>(?P<title1>.+?)</title>', html)
#if(foundTitle):
    #title = foundTitle.group("title1");
    #print "title=",title;    
##<div class="post_time_source">
##2016-11-24 13:47:00　来源: <a id="ne_article_source" href="http://www.thepaper.cn/newsDetail_forward_1567393" target="_blank" rel="nofollow">澎湃新闻网</a>(上海)        </div>
#foundPostInfo = re.search('<div\s+?class="post_time_source">\s(?P<postInfo1>.+?)\s</div>', html,re.M|re.I)
#print "foundPostInfo=",foundPostInfo
#if(foundPostInfo):
    #postInfo = foundPostInfo.group("postInfo1");
    #print "postInfo=",postInfo;   

