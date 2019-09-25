import os
import sys

from scrapy.cmdline import execute

if __name__ == '__main__':

    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    # zuida
    # execute(["scrapy", "crawl", "zuida"])
    # kuyun
    # execute(["scrapy", "crawl", "kuyun"])
    # tv
    # execute(["scrapy", "crawl", "tv"])
    # execute(["scrapy", "crawl", "tv", "-a", "keyword=CCTV-1"])
    # drama
    # execute(["scrapy", "crawl", "drama"])
    # execute(["scrapy", "crawl", "drama", "-a", "keyword=民间小调"])
    # drama_type
    # execute(["scrapy", "crawl", "drama_type"])
    # piece
    # execute(["scrapy", "crawl", "piece"])
    # piece_type
    # execute(["scrapy", "crawl", "piece_type"])
    # album
    execute(["scrapy", "crawl", "album"])