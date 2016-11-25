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
import datetime
import random

'''
②网易政务新闻数据
http://comment.news.163.com/news_gov_bbs/BTKA08A900234IG8.html
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
        self.log = Logging('./Log/log_zhengwen').get_logging()
        self.browser = self.browser_factory.create(config.browser_type)
        self.proxy = self.proxy_factory.create(config.proxy_type, config.proxy_area,
                                               config.proxy_host, config.proxy_port)
        self.queue_zhengwu = self.queue_factory.create(config.queue_type, private_config.queue_zhengwu_zhenwgen,
                                             config.queue_host, config.queue_port)
        self.queue_pinglun = self.queue_factory.create(config.queue_type, private_config.queue_pinglun,
                                             config.queue_host, config.queue_port)
        self.db = self.db_factory.create(config.db_type, config.db_table_news_zhengwen,
                                         config.db_host, config.db_port)

    def main(self):
        while(True):
            url = self.queue_zhengwu.get()
            if url:
                self.ParsePage(url)
            else:
                self.log.info('new queue is empty!')
                break
            time.sleep(random.randint(10,20))

    def ParsePage(self,url):
        try:
            html = self.browser.visit(url,encoding='gbk')
            if html:
                field =self.field_factory.create('si_chuan_news')
                tree=etree.HTML(html)
                #栏目
                lanmu = tree.xpath('.//span[@class="ep-crumb JS_NTES_LOG_FE"]/a/text()')
                #标题
                biaoti = self.textxpath(tree,'.//head/title/text()')
                #关键词
                guanjianci = self.textxpath(tree,'.//head/meta[@name="keywords"]/@content')
                #发布时间
                shijian = self.textxpath(tree,'.//div[@class="ep-time-soure cDGray"]/text()')
                timestamp=0
                if shijian:
                    shijian = re.findall('\d{4}-\d{1,2}-\d{1,2} \d{2}:\d{2}:\d{2}',shijian)[0]
                    timestamp = self.datatransform(shijian)
                #文章来源
                laiyuan = self.textxpath(tree,'.//div[@class="ep-time-soure cDGray"]/a/text()')
                #正文
                wen_zhang_zheng_wen = xpathutil.get_Node_text(tree,'.//div[@id="endText"]/p')
                #图片链接
                tu_pian_lian_jie = tree.xpath('.//div[@id="endText"]/p/img/@src')
                #评论数
                ping_lun_shu_liang = self.GetPinglun(url)

                field.set('wen_zhang_wang_zhi',url)
                field.set('wen_zhang_lan_mu',' '.join(lanmu))
                field.set('wen_zhang_biao_ti',biaoti)
                field.set('guan_jian_ci',guanjianci)
                field.set('fa_bu_shi_jian',timestamp)#时间戳格式
                field.set('wen_zhang_lai_yuan',laiyuan)
                field.set('wen_zhang_zheng_wen',wen_zhang_zheng_wen)
                field.set('tu_pian_lian_jie',tu_pian_lian_jie)
                field.set('ping_lun_shu_liang',ping_lun_shu_liang)
                field.set('id',url)
                data =field.make()
                if data:
                    # print json.dumps(data,ensure_ascii=False)
                    self.db.put(data)
                    self.log.info('save data sucess!')
            else:
                self.log.info('Parsing page wrong!')
        except Exception as e:
            self.log.info(e)
            print url#打印出解析错误的页面
            time.sleep(10)


    def GetPinglun(self,url):
        #http://news.163.com/16/0808/14/BTV3ABLP00014AEE.html
        pinglunshu=0
        try:
            uid = url.split('.html')[0].split('/')[-1]
            comment_url = 'http://sdk.comment.163.com/api/v1/products/a2869674571f77b5a0867c3d71db5856/threads/%s'%uid
            html=self.browser.visit(comment_url)
            data =json.loads(html)
            if data["tcount"]!=0:
                pinglunshu =  data["tcount"]
                uid =data["docId"]
                comment_url = 'http://comment.news.163.com/news_gov_bbs/%s.html'%uid
                # print comment_url
                self.queue_pinglun.put(comment_url+'@@@@@@'+url)
        except Exception as e:
            self.log.info('get pinglunshu wrong!%s'%e)
        return pinglunshu


    def textxpath(self, tree, path, pos=0):
        texts = tree.xpath(path)
        if not texts:
            return None
        try:
            return map(lambda x: x.strip(), filter(lambda x: x.strip(), texts))[pos]
        except:
            return None

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
            time.sleep(60*60*12)
        except Exception as e:
            consumer.log.info(e)
            time.sleep(60*5)
