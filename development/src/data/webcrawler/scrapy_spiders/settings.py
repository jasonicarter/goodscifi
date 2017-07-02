# -*- coding: utf-8 -*-

# Scrapy settings for scrapy_spiders project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'scrapy_spiders'

SPIDER_MODULES = ['scrapy_spiders.spiders']
NEWSPIDER_MODULE = 'scrapy_spiders.spiders'

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 0.25 # 250 ms of delay

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
# ITEM_PIPELINES = {
#    'scrapy_spiders.pipelines.ScrapySpidersPipeline': 300,
# }

# Configure logs
LOG_LEVEL = 'INFO'
