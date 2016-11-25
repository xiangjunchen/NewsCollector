# -*- coding: utf-8 -*-
'''
parse the weibo.cn page,faster than PC page
'''
import sys

reload(sys)
sys.setdefaultencoding('utf-8')
sys.path.append("../")

from SpiderInterface.field.FieldFactory import FieldFactory
from SpiderInterface.queue.QueueFactory import QueueFactory
from SpiderInterface.browser.BrowserFactory import BrowserFactory
from SpiderInterface.proxy.ProxyFactory import ProxyFactory
from SpiderInterface.log.Logging import Logging
from common import config
from lxml import etree
import time
import datetime
import private_config
import random
import json
import re


'''
①爬取了网易新闻下的：要问，奥运，社会，全国，国内，国际，财经，军事板块
爬取了网易政务下的：中央政务，地方建设，经济发展，文化中国
在爬取正文链接的同时也爬取到了部分评论链接self.queue_pinglun.put(commenturl+'@@@@@@'+docurl)

'''


class Zhengwen_producer(object):

    def __init__(self):
         # 实例化工厂对象
        self.queue_factory = QueueFactory()
        self.browser_factory = BrowserFactory()
        self.proxy_factory = ProxyFactory()
        # 实例化具体对象
        self.log = Logging('./Log/log_zhengwen').get_logging()
        self.browser = self.browser_factory.create(config.browser_type)
        self.proxy = self.proxy_factory.create(config.proxy_type, config.proxy_area,
                                               config.proxy_host, config.proxy_port)
        self.queue_news = self.queue_factory.create(config.queue_type, private_config.queue_news,
                                             config.queue_host, config.queue_port)
        self.queue_zhengwu = self.queue_factory.create(config.queue_type, private_config.queue_zhengwu_zhenwgen,
                                             config.queue_host, config.queue_port)
        self.queue_pinglun = self.queue_factory.create(config.queue_type, private_config.queue_pinglun,
                                             config.queue_host, config.queue_port)


    def main(self):
        lanmu_list=self.get_lanmu()
        # lanmu_list=['http://public.house.163.com/special/03531F4E/index_news.js?callback=data_callback']
        try:
            for url in lanmu_list:
                if 'gov' in url:
                    self.getGovHref(url)
                else:
                    self.getNewsHref(url)
                # time.sleep(random.randint(10,20)
            self.log.info('getting the zhengwen href successful!')
        except Exception as e:
            self.log.info(e)
            time.sleep(10)


    def getNewsHref(self,url):
        #获取网易新闻正文链接
        url_l = url
        page=2
        try:
            while(True):
                # print url_l
                html = self.browser.visit(url_l,encoding='gbk')
                if html:
                    html = html.replace(' ','').replace('\n','')
                    html = str(html).replace('data_callback([','{"data":[').replace('])',']}')
                    html = re.sub(r",\s*?]", "]", html)
                    datas = json.loads(html,encoding='utf-8')
                    for data in datas['data']:
                        # print data
                        docurl=data['docurl']#正文链接
                        commenturl = data['commenturl']#评论链接
                        # print docurl,commenturl
                        if commenturl:
                            self.queue_pinglun.put(commenturl+'@@@@@@'+docurl)
                        else:
                            uid = docurl.split('.html')[0].split('/')[-1]
                            commenturl = 'http://comment.news.163.com/news3_bbs/%s.html'%uid
                            self.queue_pinglun.put(commenturl+'@@@@@@'+docurl)
                        self.queue_news.put(docurl)
                else:
                    break
                url_l = url.split('.js?')[0]+'_%s.js' %str(page).zfill(2)
                page+=1
        except Exception as e:
            self.log.info(e)

    def getGovHref(self,url):
        #获取网易政务新闻链接
        url_l =url
        #http://gov.163.com/special/zwzx_n/;http://gov.163.com/special/zwzx_n_02/
        try:
            if 'zwzx' in url:
                totalpage=17
            else:
                totalpage =5
            for page in xrange(2,totalpage):
                html = self.browser.visit(url_l,encoding='gbk')
                tree = etree.HTML(html)
                hrefs = tree.xpath('.//div[@class="cnt"]/ul/li/a/@href')
                # print len(hrefs)
                if hrefs:
                    for href in hrefs:
                        # print href
                        self.queue_zhengwu.put(href)
                url_l = url[0:-1]+'_%s/'%str(page).zfill(2)
        except Exception as e:
            self.log.info(e)

    def get_lanmu(self):
        #从lanmu_href文件读入栏目链接
        lanmu_hrefs=[]
        file = open('lanmu_href','r')
        for line in file.readlines():
            lanmu_hrefs.append(line.split('\n')[0])
        return lanmu_hrefs

    def textxpath(self, tree, path, pos=0):
        texts = tree.xpath(path)
        if not texts:
            return None
        try:
            return map(lambda x: x.strip(), filter(lambda x: x.strip(), texts))[pos]
        except:
            return None


if __name__ == '__main__':
    producer = Zhengwen_producer()
    while(True):
        try:
            producer.main()
            time.sleep(60*60*6)
        except Exception as e:
            producer.log.info(e)
            time.sleep(60)
