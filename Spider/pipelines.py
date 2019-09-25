# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from Spider.util.MongoDbUtils import MongoDbUtils
from Spider.util.TypeUtils import TypeUtils

# 将爬取到的数据保存到数据库
class MovieSpiderPipeline(object):
    def process_item(self, item, spider):
        # 申请资源
        collection = 'movie'
        db_utils = MongoDbUtils(collection)
        # 执行 sql
        # 将 tuple 类型转换为字符串
        for field in item.fields:
            if TypeUtils.typeof(item[field]) == 'tuple':
                item[field] = item[field][0]
        db_utils.insert(dict(item))
        return item

# 将爬取到的数据保存到数据库
class ZuidaSpiderPipeline(object):
    def process_item(self, item, spider):
        # 申请资源
        collection = 'movie'
        db_utils = MongoDbUtils(collection)
        # 执行 sql
        item = dict(item)
        movie_id = item['id']
        movie_name = item['name']
        dic = {'id': movie_id}
        dic2 = {'name': movie_name}
        movies1 = db_utils.find(dic)
        movies2 = db_utils.find(dic2)
        # 服务器中资源中的最大集数
        max1 = 0
        # 新爬取视频中资源中的最大集数
        max2 = 0
        if (movies1.count() > 0):
            # 当前视频已爬取且更新，将新爬去的数据更新到数据库
            movies1_temp = movies1.__getitem__(0)
            index1 = 0
            index2 = 0
            for source in movies1_temp['sources']:
                if (item['sources'][index1]['name'] == movies1_temp['sources'][index2]['name']):
                    movies1_temp['sources'][index2] = item['sources'][index1]
                    index1 += 1
                    index2 += 1
                else: index2 += 1
            newdic = {'$set': {'update_status': item['update_status'], 'sources': movies1_temp['sources']}}
            db_utils.update(dic, newdic)
        elif (movies2.count() > 0):
            # 新的资源网站爬取到的电影数据，且电影已存在数据库中，将新的资源添加到当前电影的资源中，
            # 如果爬取的视频的最大集数大于服务器中当前视频的最大集数，则更新服务器中当前视频的更新状态
            movies2_temp = movies2.__getitem__(0)
            index1 = 0
            index2 = 0
            for source in movies2_temp['sources']:
                if (item['sources'][index1]['name'] == movies2_temp['sources'][index2]['name']):
                    movies2_temp['sources'][index2] = item['sources'][index1]
                    index1 += 1
                    index2 += 1
                else:
                    index2 += 1
            if (index1 == 0): movies2_temp['sources'] += item['sources']
            newdic = {'$set': {'update_status': item['update_status'], 'sources': movies2_temp['sources']}}
            db_utils.update(dic2, newdic)
        else: db_utils.insert(item)
        return item

# 将爬取到的数据保存到数据库
class MovieTypeSpiderPipeline(object):
    def process_item(self, item, spider):
        # 申请资源
        collection = 'movie_type'
        db_utils = MongoDbUtils(collection)
        # 执行 sql
        db_utils.insert(dict(item))
        return item

# 将爬取到的数据保存到数据库
class MovieSourceSpiderPipeline(object):
    def process_item(self, item, spider):
        # 申请资源
        collection = 'movie'
        db_utils = MongoDbUtils(collection)
        # 执行 sql
        dic = {'id': item['id']}
        new_dic = {'$set': {'sources': item['sources']}}
        db_utils.update(dic, new_dic)
        return item

# 将爬取到的数据保存到数据库
class TvSpiderPipeline(object):
    def process_item(self, item, spider):
        # 申请资源
        collection = 'tv'
        db_utils = MongoDbUtils(collection)
        # 执行 sql
        db_utils.insert(dict(item))
        return item
