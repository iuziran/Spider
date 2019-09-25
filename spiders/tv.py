# -*- coding: utf-8 -*-
import time

import scrapy
from lxml import etree
from selenium import webdriver

from Spider.items import *
from Spider.util.CommonUtils import *

# 电视爬虫
from Spider.util.MongoDbUtils import MongoDbUtils

# 删除电视资源
def remove_tv(name):
    collection = 'tv'
    db_utils = MongoDbUtils(collection)
    dict = {'name': name}
    db_utils.delete(dict)

class TvSpider(scrapy.Spider):
    name = 'tv'
    allowed_domains = ['www.icantv.cn']
    orign_url = 'http://www.icantv.cn'
    list_origin_url = orign_url + '/tvlist'
    start_urls = []
    search_domain = 'http://www.icantv.cn/search.php'
    # 搜索关键词
    keyword = None
    type = 'tv'
    driver = None

    def __init__(self, target=None, keyword=None, name=None, **kwargs):
        super(TvSpider, self).__init__(name, **kwargs)
        self.driver = get_driver(1)
        self.driver.minimize_window()
        if keyword is not None:
            # 搜索指定影视
            self.keyword = keyword
            first_search_url = self.search_domain + '?page=1&keyword=' + keyword
            self.start_urls.append(first_search_url)
        else:
            self.start_urls.append(self.list_origin_url + '/all.html')
        # 获取总页数、总条数
        total_page = 0
        total = 0
        page_size = 30
        html = get_one_page(self.start_urls[0])
        html = etree.HTML(html)
        for each in html.xpath("//span[@class='pageinfo']"):
            total_page = each.xpath("./strong[1]/text()")[0]
            total = each.xpath("./strong[2]/text()")[0][1:]

            # 将每页的地址添加到 start_urls
            if self.keyword is not None:
                for page in range(2, (int)(total_page) + 1):
                    self.start_urls.append(self.search_domain + '?page='+(str)(page)+'&keyword=' + keyword)
            else:
                for page in range(2, (int)(total_page) + 1):
                    self.start_urls.append(self.list_origin_url + '/all/' + str(page) + '.html')

    custom_settings = {
        'ITEM_PIPELINES': {
            'Spider.pipelines.TvSpiderPipeline': 300,
        }
    }


    def parse(self, response):

        # 获取所有电影的 id，用于判断电影是否已经爬取
        collection = 'tv'
        db_utils = MongoDbUtils(collection)
        dict = [{}, {'name': 1}]
        data = db_utils.find(dict)
        tv_names = []
        for tv_name in data:
            tv_names.append(tv_name['name'])
        for each in response.xpath("//ul[@class='tv']"):
            for each2 in each.xpath("./li"):
                url = each2.xpath("./a/@href").extract()[0]
                self.driver.get(self.orign_url + url)
                html = self.driver.page_source
                html2 = etree.HTML(html)
                pattern = '[\s\S]*?<a href="/tvlist/[\s\S]*?>([\s\S]*?)</a>[\s\S]*?&gt; ([\s\S]*?)在线直播[\s\S]*?<div class="content 7">[\s\S]*?src="([\s\S]*?)"[\s\S]*?>([\s\S]*?)</div>'
                tv_item = TvItem()
                for tmp_tv_item in parse_one_page(html, pattern):
                    tv_item['type'] = tmp_tv_item[0]
                    tv_item['name'] = tmp_tv_item[1]
                    dic = {'name': tv_item['name']}
                    if db_utils.find(dic).count() > 0:
                        print(tv_item['name'] + ' 已抓取')
                        break
                    tv_item['src'] = tmp_tv_item[2]
                    tv_item['introduction'] = tmp_tv_item[3]
                    pattern2 = '[\s\S]*?<span onclick="sw_play([\s\S]*?)">([\s\S]*?)</span>'
                    sources = []
                    for tmp_tv_source in parse_one_page(html, pattern2):
                        tmp_tv_source_index = (int)(tmp_tv_source[0].split('(')[1].split(')')[0]) + 1
                        tmp_tv_source_name = tmp_tv_source[1]
                        self.driver.find_element_by_xpath('/html/body/div[3]/div[1]/div[2]/div[1]/span['+(str)(tmp_tv_source_index)+']').click()
                        iframe = self.driver.find_element_by_xpath('//*[@id="play_player"]/div/iframe')
                        self.driver.switch_to_frame(iframe)
                        time.sleep(2)
                        html = self.driver.page_source
                        pattern4 = '[\s\S]*?var u = "([\s\S]*?)"[\s\S]*?'
                        source_url = ''
                        if 'var u = ' in html:
                            for tmp_play_url in parse_one_page(html, pattern4):
                                source_url = tmp_play_url
                            source = {'name': tmp_tv_source_name, 'url': source_url}
                            sources.append(source)
                            print('正在抓取 -> ' + tv_item['name'] + ' ' + source['name'])
                        else:
                            print(tv_item['name'] + ' ' + tmp_tv_source_name + ' -> 没有相应资源')
                        print('切换到主frame')
                        self.driver.switch_to.parent_frame()
                    tv_item['sources'] = sources
                    yield tv_item