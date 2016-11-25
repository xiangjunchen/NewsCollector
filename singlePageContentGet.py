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
        #comment_url = 'http://comment.news.163.com/%s/%s.html'%group%uid
        print title
        print commentCount        
    return title,commentCount
ParserCommentPage('http://news.163.com/16/1124/13/C6L2K0IP000187VE.html')