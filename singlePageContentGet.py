#coding:utf-8  
import urllib2
import json
import MySQLdb

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
    sRe += SaveToDB(data)
    return sRe
def SaveToDB(data):
    #需要判断当前待加入条目是否已经在库中存在，通过post_url_src查询判断
    # 打开数据库连接
    db = MySQLdb.connect("localhost","root","123","weiyue" )   
    # 使用cursor()方法获取操作游标 
    cursor = db.cursor()
    
    # SQL 插入语句
    sql = """INSERT INTO wy_posts(post_date,
             post_content, post_title, comment_count, post_url_src)
             VALUES (data["createTime"], data["title"], data["title"], data["tcount"],data["url"])"""
    try:
        # 执行sql语句
        cursor.execute(sql)
        # 提交到数据库执行
        db.commit()
        #最近一次新增自动增长ID
        print conn.insert_id()
        print "content save to db success !"
    except:
        # Rollback in case there is any error
        db.rollback()
    
    # 关闭数据库连接
    db.close()
    return "content save to db success !"
    
sRe = ParserCommentPage("http://news.163.com/16/1125/10/C6N9F2L600014JB6.html")
print sRe