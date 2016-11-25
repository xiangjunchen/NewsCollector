# -*- coding: utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf-8')
sys.path.append("../")

from SpiderInterface.field.FieldFactory import FieldFactory
from SpiderInterface.queue.QueueFactory import QueueFactory
from SpiderInterface.browser.BrowserFactory import BrowserFactory
from SpiderInterface.proxy.ProxyFactory import ProxyFactory
from SpiderInterface.log.Logging import Logging
from lxml import etree
from common import config
from common import xpathutil
import private_config
import re
import time
import json
import random

'''
③获取评论数据
pinglun_url=http://comment.news.163.com/news_gov_bbs/BTHNT83600234IG8.html
'''

class Zhengwen_consumer():

    def __init__(self):
         # 实例化工厂对象
        self.field_factory = FieldFactory(u'网易新闻')
        self.queue_factory = QueueFactory()
        self.browser_factory = BrowserFactory()
        self.proxy_factory = ProxyFactory()
        self.db_factory = QueueFactory()

        # 实例化具体对象
        self.log = Logging('./Log/log_pinglun').get_logging()
        self.browser = self.browser_factory.create(config.browser_type)
        self.proxy = self.proxy_factory.create(config.proxy_type, config.proxy_area,
                                               config.proxy_host, config.proxy_port)
        self.queue_pinglun = self.queue_factory.create(config.queue_type, private_config.queue_pinglun,
                                             config.queue_host, config.queue_port)
        self.db = self.db_factory.create(config.db_type, config.db_table_news_zhengwen,
                                         config.db_host, config.db_port)

    def main(self):
        while(True):
            url = self.queue_pinglun.get()
            if url:#http://comment.news.163.com/news_gov_bbs/BTHNT83600234IG8.html
                comment_url,self.docurl=url.split('@@@@@@')
                # comment_url,self.docurl=['http://comment.news.163.com/news3_bbs/BTSJOECA00014SEH.html','url']
                try:
                    if comment_url:
                        self.GetPage(comment_url)
                except Exception as e:
                    self.log.info(e)
                    # print comment_url#打印出解析错误的页面
            else:
                self.log.info('new queue is empty!')
                break
            time.sleep(random.randint(10,20))


    def GetPage(self,comment_url):
        uid = comment_url.split('.html')[0].split('/')[-1]
        offset = 0
        limit = 30
        while(True):
            js_url = 'http://comment.news.163.com/api/v1/products/a2869674571f77b5a0867' \
                     'c3d71db5856/threads/%s/comments/newList?offset=%s&limit=%s'%(uid,str(offset),str(limit))
            html = self.browser.visit(js_url)
            datas = json.loads(html)
            newListSize =datas["newListSize"]
            if newListSize!=0:
                self.ParseData(datas)
                limit = 30
                offset += limit
                time.sleep(random.randint(5,10))
            else:
                # self.log.info('Parsing page wrong!')
                break

    def ParseData(self,datas):
        commentIds = datas['commentIds']
        comments = datas['comments']
        for ids in commentIds:
            idList=ids.split(',')
            id_n = idList[-1]#最后一个id为当前帖子的id
            field =self.field_factory.create('ping_lun')
            # 评论文章链接
            field.set('news_url',self.docurl)
            #评论时间戳
            time=comments[id_n]['createTime']
            field.set('ping_lun_shi_jian',self.datatransform(time))
            # 回复数量
            field.set('hui_fu_shu',0)
            # 点赞数量
            field.set('dian_zan_shu',comments[id_n]['vote'])
            #评论id
            field.set('ping_lun_id',id_n)
            # 用户昵称
            field.set('yong_hu_ming',comments[id_n]['user']['nickname'])
            # 用户省份
            field.set('yong_hu_sheng_fen',comments[id_n]['user']['location'])#时间戳格式
            # 评论内容
            content_all =u''
            for id in idList:
                if id in comments.keys():
                    content=comments[id]['content']
                    content_all+=content
            field.set('ping_lun_nei_rong',content_all)
            field.set('id',id_n)
            data =field.make()
            if data:
                # print json.dumps(data,ensure_ascii=False)
                self.db.put(data)
                self.log.info('save data sucess!')

    def datatransform(self, data):
        #将年月日转换为时间戳2016-08-08 10:01:56

        timeStamp=time.mktime(time.strptime(data,'%Y-%m-%d %H:%M:%S'))
        # if not data:
        #     data = '2016-01-02'
        # data=data.decode('gbk')
        # timeArray = data.split('-')
        # d = datetime.datetime(int(timeArray[0]), int(timeArray[1]), int(timeArray[2]))
        # timeStamp=int(time.mktime(d.timetuple()))
        return timeStamp



if __name__ == '__main__':
    consumer = Zhengwen_consumer()
    while(True):
        try:
            consumer.main()
            time.sleep(60*60*2)
        except Exception as e:
            consumer.log.info(e)
            time.sleep(60*5)
