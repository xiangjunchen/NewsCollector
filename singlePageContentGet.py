#coding:utf-8  
import urllib2
import json
import MySQLdb
import time
import random

def ParserContentPage(urlContent):
    #urlContent = http://news.163.com/16/0808/14/BTV3ABLP00014AEE.html
    title=''
    commentCount=0     
    uid = urlContent.split('.html')[0].split('/')[-1]
    contenturl = 'http://comment.news.163.com/api/v1/products/a2869674571f77b5a0867c3d71db5856/threads/%s'%uid
    #headers = {'User-agent' : 'Mozilla/5.0 (Windows NT 6.2; WOW64; rv:22.0) Gecko/20100101 Firefox/22.0'}
    #request = urllib2.Request(contenturl, headers = headers)  
    response = urllib2.urlopen(contenturl)        
    html = response.read()
    data =json.loads(html)
    response.close()
    if data["tcount"]!=0:
        title = data["title"]
        commentCount = data["tcount"]
        group = data["boardId"]
    sRe = "parser success ! comment count is "+str(commentCount)+"\r\n"
    sql = GetContentInsertSqlStr(data)
    insertId = SaveToDB(sql,data)
    if insertId != 0:
        ParserCommentPage(urlContent,insertId)        
    else:
        sRe = "ContentSaveToDB failed!"
    return sRe
def SaveToDB(sql,data):
    #需要判断当前待加入条目是否已经在库中存在，通过post_url_src查询判断
    # 打开数据库连接
    db = MySQLdb.connect("localhost","root","123","weiyue" )   
    db.set_character_set('utf8')
    # 使用cursor()方法获取操作游标 
    cursor = db.cursor()
    # 使用execute方法执行SQL语句
    #cursor.execute("SELECT VERSION()")    
    # 使用 fetchone() 方法获取一条数据库。
    #data = cursor.fetchone()    
    #print "Database version : %s " % data    
    # SQL 插入语句 
    insertId = 0;
    try:
        # 执行sql语句
        cursor.execute(sql)
        insertId = cursor.lastrowid
        print "ID of last record is ", int(cursor.lastrowid) #最后插入行的主键ID
        print "ID of inserted record is ", int(db.insert_id()) #最新插入行的主键ID，conn.insert_id()一定要在conn.commit()之前，否则会返回0        
        # 提交到数据库执行
        db.commit()
        outputstr = " save to db success !"
    except MySQLdb.Warning, w:  
        outputstr =  "Warning:%s" % str(w)      
    except MySQLdb.Error, e:  
        try:  
            outputstr =  "Error %d:%s" % (e.args[0], e.args[1])  
        except IndexError:  
            outputstr = "MySQL Error:%s" % str(e)     
        db.rollback()    
    # 关闭数据库连接
    db.close()
    return insertId 
def GetContentInsertSqlStr(data):
    #sql = "INSERT INTO wy_posts(post_content) VALUES ('%s')" % (data["title"])       
    sql = "INSERT INTO wy_posts(post_author,post_date,post_date_gmt,post_content,post_title,post_excerpt,\
            post_status,comment_status,ping_status,post_password,post_name,to_ping,pinged,post_modified,\
            post_modified_gmt,post_content_filtered,post_parent,guid,menu_order,post_type,post_mime_type,\
            comment_count,collect_count,forward_count,post_url_src,post_gps) VALUES ('%d','%s','%s','%s','%s',\
            '%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%d','%s','%d','%s','%s','%d','%d','%d','%s',\
            '%d')" % (1,data["createTime"],data["createTime"],data["title"],data["title"],data["title"],'publish',\
            'open','open','','','','',data["modifyTime"],data["modifyTime"],'',0,data["url"],0,'post','',\
            int(data["tcount"]),0,0,data["url"],0)
    return sql    
def ParserCommentData(datas,postContentId,parseCount):
    commentIds = datas['commentIds']
    comments = datas['comments']
    for ids in commentIds:
        idList=ids.split(',')
        id_n = idList[-1]#最后一个id为当前帖子的id
        #field =self.field_factory.create('ping_lun')
        # 评论文章链接
        #field.set('news_url',self.docurl)
        #评论时间戳
        time=comments[id_n]['createTime']
        #field.set('ping_lun_shi_jian',self.datatransform(time))
        # 回复数量
        #field.set('hui_fu_shu',0)
        # 点赞数量
        #field.set('dian_zan_shu',comments[id_n]['vote'])
        #评论id
        #field.set('ping_lun_id',id_n)
        # 用户昵称
        #field.set('yong_hu_ming',comments[id_n]['user']['nickname'])
        # 用户省份
        #field.set('yong_hu_sheng_fen',comments[id_n]['user']['location'])#时间戳格式
        # 评论内容
        content_all =u''
        #for id in idList:
            #if id in comments.keys():
                #content=comments[id]['content']
                #print content
                #content_all+=content
            
        parseCount += 1     
        if(comments[id_n]['vote'] > 100):
            print comments[id_n]['content']
        print str(comments[id_n]['vote'])+'   current ' + str(parseCount)
        if(parseCount < 100):
            sql = GetCommentInsertSqlStr(postContentId, comments[id_n])
            SaveToDB(sql, comments[id_n])
        #print content_all
        #field.set('ping_lun_nei_rong',content_all)
        #field.set('id',id_n)
        #data =field.make()
        #if data:
            ## print json.dumps(data,ensure_ascii=False)
            #self.db.put(data)
            #self.log.info('save data sucess!')
    return parseCount
def GetCommentInsertSqlStr(postContentId, data):
    sql = "INSERT INTO wy_comments_0(comment_post_ID,comment_author,comment_author_email,comment_author_url,\
                comment_author_IP,comment_date,comment_date_gmt,comment_content,comment_karma,comment_approved,\
                comment_agent,comment_type,comment_parent,user_id,comment_gps,comment_thumbsup,comment_despise,\
                comment_up_count,comment_down_count,comment_user_location) VALUES ('%d','%s','%s','%s','%s','%s','%s','%s','%d','%s','%s',\
                '%s','%d','%d','%d','%d','%d','%d','%d','%s')" % (postContentId,'testUser','','',data["ip"],\
                data["createTime"],data["createTime"],data["content"], 0,'','','',0,data["user"]["userId"],0,0,0,data["vote"],0,data["user"]["location"])
    return sql
def ParserCommentPage(urlContent,postContentId):
    uid = urlContent.split('.html')[0].split('/')[-1]
    offset = 0
    limit = 30
    #time.sleep(random.randint(5,10))
    parseCount = 0
    while(True):
        comment_url = 'http://comment.news.163.com/api/v1/products/a2869674571f77b5a0867' \
            'c3d71db5856/threads/%s/comments/newList?offset=%s&limit=%s'%(uid,str(offset),str(limit))
        headers = {'User-agent' : 'Mozilla/5.0 (Windows NT 6.2; WOW64; rv:22.0) Gecko/20100101 Firefox/22.0'}
        request = urllib2.Request(comment_url, headers = headers)        
        response = urllib2.urlopen(request)
        html = response.read()
        datas = json.loads(html)
        response.close()
        newListSize =datas["newListSize"]        
        if newListSize!=0:
            parseCount = ParserCommentData(datas,postContentId,parseCount)
            limit = 30
            offset += limit
            time.sleep(random.randint(5,10))
        else:
            # self.log.info('Parsing page wrong!')
            break    
    print "ParserCommentPage end"
    return

sRe = ParserContentPage("http://news.163.com/16/1125/10/C6N9F2L600014JB6.html")
print sRe