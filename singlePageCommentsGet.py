#coding:gbk 
import urllib2  
import re  
import json  
import time
import random
#用户id+评论+顶  
def GetPage(comment_url):
    uid = comment_url.split('.html')[0].split('/')[-1]
    offset = 0
    limit = 30
    while(True):
        js_url = 'http://comment.news.163.com/api/v1/products/a2869674571f77b5a0867' \
            'c3d71db5856/threads/%s/comments/newList?offset=%s&limit=%s'%(uid,str(offset),str(limit))
        #js_url = comment_url
        response = urllib2.urlopen(js_url)
        html = response.read()
        datas = json.loads(html)
        newListSize =datas["newListSize"]
        if newListSize!=0:
            ParseData(datas)
            limit = 30
            offset += limit
            time.sleep(random.randint(5,10))
        else:
            # self.log.info('Parsing page wrong!')
            break

def ParseData(datas):
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
        for id in idList:
            if id in comments.keys():
                content=comments[id]['content']
                content_all+=content
        #print content_all
        #field.set('ping_lun_nei_rong',content_all)
        #field.set('id',id_n)
        #data =field.make()
        #if data:
            ## print json.dumps(data,ensure_ascii=False)
            #self.db.put(data)
            #self.log.info('save data sucess!')

def datatransform(data):
    #将年月日转换为时间戳2016-08-08 10:01:56

    timeStamp=time.mktime(time.strptime(data,'%Y-%m-%d %H:%M:%S'))
    # if not data:
    #     data = '2016-01-02'
    # data=data.decode('gbk')
    # timeArray = data.split('-')
    # d = datetime.datetime(int(timeArray[0]), int(timeArray[1]), int(timeArray[2]))
    # timeStamp=int(time.mktime(d.timetuple()))
    return timeStamp
GetPage("http://sports.163.com/16/1125/10/C6N8K85J0005877V.html")
print "end "