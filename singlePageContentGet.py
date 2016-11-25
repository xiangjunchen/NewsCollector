#coding:utf-8  
import urllib2
import json

def ParserCommentPage(urlContent):
    #urlContent = http://news.163.com/16/0808/14/BTV3ABLP00014AEE.html
    title=''
    commentCount=0     
    uid = urlContent.split('.html')[0].split('/')[-1]
    comment_url = 'http://comment.news.163.com/api/v1/products/a2869674571f77b5a0867c3d71db5856/threads/%s'%uid
    response = urllib2.urlopen(comment_url)        
    html = response.read()
    data =json.loads(html)
    if data["tcount"]!=0:
        title = data["title"]
        commentCount = data["tcount"]
        group = data["boardId"]
    sRe = "parser success ! comment count is "+str(commentCount)+"\r\n"
    
    sRe += "content save to db success ! "
    return sRe
    
sRe = ParserCommentPage("http://news.163.com/16/1125/10/C6N9F2L600014JB6.html")
print sRe