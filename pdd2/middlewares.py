# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
import MySQLdb
import random
# global count
# count = 1

class Pdd2SpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


# 设置代理IP
class ProxyMiddleware(object):
    # overwrite process request
    def process_request(self, request, spider):
         # 数据库查找可用代理IP
         # global count
         conn = MySQLdb.connect("localhost", "root", "123456", "ip_pool")
         cursor = conn.cursor()
         cursor.execute("select ip from ip_table")
         data = cursor.fetchall()
         ip = random.choice(data)
         print '使用IP:', ip[0]
         # print '计数: %d' % count
         # count += 1
         cursor.close()
         conn.close()
         # Set the location of the proxy
         request.meta['proxy'] = ip[0]

         # 禁止重定向
         request.meta['dont_redirect'] = True
         # request.meta['handle_httpstatus_list'] = [302]
         request.meta['handle_httpstatus_list'] = [500, 502, 503, 504, 408, 301, 302, 304, 400, 401, 403, 404, 404]

# yield Request(item['link'],meta = {
#                   'dont_redirect': True,
#                   'handle_httpstatus_list': [302]
#               }, callback=self.your_callback)
