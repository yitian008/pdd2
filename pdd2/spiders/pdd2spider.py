# -*- coding: utf-8 -*-
#!/usr/bin/env python

import scrapy
from pdd2.items import Pdd2Item
import re
import time

class Pdd2spiderSpider(scrapy.Spider):
    name = "pdd2spider"
    # handle_httpstatus_list = [500, 502, 503, 504, 408, 301, 302, 304, 400, 401, 403, 404]
    allowed_domains = ["www.panduoduo.net"]
    start_urls = ['http://www.panduoduo.net/bd/1']

    def parse(self, response):
        print '状态码为: ', response.status
        print 'h1 is :', response.css('h1::text').extract_first()
        print response.body
        if response.status == 200:
            # print '检查页面元素: ', response.css('div.container span.name a::text')
            urls = response.css('a.blue::attr(href)').extract()
            print '共有%d个网页等待下载...' % len(urls)
            if len(urls) == 0:
                # 正常的话有180个a
                urls = response.css('div.content a::attr(href)').extract()
                # 每个div中只取第一个a
                urls = urls[::3]
            print '共有%d个网页等待下载...' % len(urls)







            # tests = response.css('div.page-list a::attr(href)').extract()
            # print 'tests:\n', tests
            # for url in urls:
            for url in urls[:10]:
                url = 'http://www.panduoduo.net' + url
                yield scrapy.Request(url, callback=self.parse_detail, meta={'url':url, \
                                                                            'dont_redirect': True, \
                                                                            'handle_httpstatus_list': [500, 502, 503, 504, 408, 301, 302, 304, 400, 401, 403, 404]})
            # next_page_url = 'http://www.panduoduo.net' + response.css('div.page-list a::attr(href)').extract()[-2]
            # print 'next_page_url is : ', next_page_url
            # if next_page_url is not None:
            #     yield scrapy.Request(next_page_url, callback=self.parse)

    def parse_detail(self, response):
        print '详细页面状态码: ', response.status
        print 'h1 is :', response.css('h1::text').extract_first()

        if response.status == 200:
            print response.body
            item = Pdd2Item()
            all_dd = response.css('dd')
            if len(all_dd) > 7:
                dd0 = all_dd[0]  # 分享用户 share_user
                dd1 = all_dd[1]  # 资源分类 file_class
                dd2 = all_dd[2]  # 文件大小 file_size
                # dd3 = all_dd[3]  # 资源类型 百度网盘
                # dd4 = all_dd[4]  # 浏览次数
                dd5 = all_dd[5]  # 发布日期 share_time
                dd6 = all_dd[6]  # 资源类别 ford
                # dd7 = all_dd[7]  # 其他

                item['share_user_bd_id'] = dd0.css('a::attr(href)').extract_first()[6:]
                item['share_user'] = dd0.css('a::text').extract_first()
                # item['file_class'] = dd1.css('a::text').extract_first()
                item['file_size'] = dd2.css('b::text').extract_first()
                item['share_time'] = dd5.css('::text').extract_first()[5:]
                # item['ford'] = dd6.css('::text').extract_first()[5:]
                item['title'] = response.css('h1::text').extract_first()
                share_url = response.css('a.dbutton2::attr(href)').extract_first()
                share_url = re.compile('http%3A.*').findall(share_url)[0]
                share_url = share_url.replace('%3A', ':').replace('%3F', '?').replace('%3D', '=').replace('%26', '&')
                item['share_url'] = share_url

                # 控制采集速度
                # time.sleep(0.5)
                yield item

            else:
                target = response.css('div.resource-page')

                item['share_user_bd_id'] = target.css('p.sep a::attr(href)').extract_first()[6:]
                item['share_user'] = target.css('p.sep a::text').extract_first()
                item['share_time'] = target.css('p.sep::text').extract_first()# 修改
                item['file_size'] = target.css('div.sep::text').extract_first()


                share_url = target.css('a::attr(href)').extract_first()
                share_url = re.compile('http%3A.*').findall(share_url)[0]
                share_url = share_url.replace('%3A', ':').replace('%3F', '?').replace('%3D', '=').replace('%26', '&')
                item['share_url'] = share_url
                item['title'] = target.css('h1::text').extract_first()

                yield item