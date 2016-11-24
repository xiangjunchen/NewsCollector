#coding:utf-8  
import urllib2
import json
import re

response = urllib2.urlopen('http://news.163.com/16/1124/13/C6L2K0IP000187VE.html')
html = response.read()
#<title>国家食药监总局:对北京等12个省市开展水产品检查_网易新闻</title>
#<div class="post_time_source"> 
#<h1 class="h1user">crifan</h1>
foundTitle = re.search('<title>(?P<title1>.+?)</title>', html)

if(foundTitle):
    title = foundTitle.group("title1");
    print "title=",title;    
#<div class="post_time_source">
#2016-11-24 13:47:00　来源: <a id="ne_article_source" href="http://www.thepaper.cn/newsDetail_forward_1567393" target="_blank" rel="nofollow">澎湃新闻网</a>(上海)        </div>
foundPostInfo = re.search('<div\s+?class="post_time_source">(?P<postInfo>.+?)</div>', html)
print "foundPostInfo=",foundPostInfo
if(foundPostInfo):
    title = foundPostInfo.group("postInfo");
    print "postInfo=",postInfo;   
#print "foundH1user=",foundH1user;
    #foundH1user = re.search('<h1\s+?class="h1user">(?P<h1user>.+?)</h1>', respHtml);
#if(foundH1user):
    #h1user = foundH1user.group("h1user");
    #print "h1user=",h1user;
#print html
