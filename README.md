# 爬虫大全

爬虫大全集合了大家常用的爬虫，为大家日常的开发提供方便。希望大家能共同努力，让这个项目变得丰富而充实。

这个项目主要基于 ```python``` 、```scrapy``` ，数据库采用```MongoDB```数据库，采集到的数据都保存在 ```MongodbDB``` 数据库。

> 本项目仅为学习之作，请勿用作商业用途，否则后果自负！

### 功能说明

##### 最大资源网

网址为：www.zuidazy1.net，爬虫名称：zuida，主要包括各种最新影视资源

##### 酷云资源网

主要包括各种最新影视资源

##### 爱看TV

主要包括各种电视资源

### 打赏

------

- 解决上面这些问题，需要花费很多时间与精力。支持项目继续完善下去，你也可以贡献一份力量！

- 有了打赏，也就会有更新的动力 : )

  ![](image/5.jpg)

### 更新日志

------

#### v1.0.0 `2019/9/25`

- 完成项目的初始化
- 当前项目中包含的爬虫包括最大资源网(www.zuidazy1.net)、酷云资源网(www.kuyunzy1.com)、爱看TV(www.icantv.cn)、戏曲屋(www.xiqu5.com)、小品屋(www.xiaopin5.com)、QQ相册(i.qq.com)

### 开发文档[待完善]

------

#### 爬虫代码(Spider)使用方法

1、将```Spider/PocketLifeSpider/PocketLifeSpider/util```下面的```MongoDbUtils.py```中的```139.199.24.205```环卫数据库所在机器的域名或ip地址。

```python
settings = {
    # "ip":'localhost',   #ip
    "ip":'127.0.0.1',   #ip
    "port":27017,           #端口
    "db_name" : "spider",    #数据库名字
}
```

2、资源名称及其对应的命令

| 资源名称           | 命令                                   |
| ------------------ | -------------------------------------- |
| 最大资源网         | scrapy crawl zuida                     |
| 酷云资源网         | scrapy crawl kuyun                     |
| 爱看TV             | scrapy crawl tv                        |
| 爱看TV(指定关键词) | scrapy crawl tv -a keyword=CCTV-1      |
| 戏曲屋             | scrapy crawl drama                     |
| 戏曲屋(指定关键词) | scrapy crawl drama -a keyword=民间小调 |
| 戏曲屋(戏曲类型)   | scrapy crawl drama_type                |
| 小品屋             | scrapy crawl piece                     |
| 小品屋(小品类型)   | scrapy crawl piece_type                |
| QQ相册             | scrapy crawl album                     |