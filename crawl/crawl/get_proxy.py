from crawl.models import Proxy
from fake_useragent import UserAgent
from .util import TIMEOUT
import re
import random
import requests
from multiprocessing.dummy import Pool as ThreadPool
from multiprocessing import Pool
import queue
from lxml import etree
from mongoengine import *
import time
from mysite.private_settings import M_DB_NAME, M_DB_HOST, M_DB_PORT


def get_user_agent():
    '''
    随机获得一个UA
    Returns
    -------

    '''
    ua = UserAgent()
    return ua.random


def fetch(url, proxy=None, params=None):
    s = requests.Session()
    s.headers.update({'user-agent': get_user_agent()})

    proxies = None
    if proxy is not None:
        proxies = {
            'http': proxy,
        }
    return s.get(url, timeout=TIMEOUT, proxies=proxies, params=params)


def get_content_proxy(url, proxy=None, params=None):
    s = requests.Session()
    s.headers.update({'user-agent': get_user_agent()})
    if proxy:
        proxies = {
            'http': proxy
        }
    else:
        try:
            proxy = Proxy.get_random()
        except:
            pass
        if proxy:
            proxies = {
                proxy.type: proxy.address,
            }
        else:
            proxies = None
    return s.get(url, timeout=TIMEOUT, proxies=proxies, params=params)


def deal_proxies(proxies):
    print(proxies)


def deal_kuaidaili_url(url, page=1):
    # connect(M_DB_NAME, host=M_DB_HOST, port=M_DB_PORT)
    url2 = url.format(page)
    text = get_content_proxy(url2).text
    html = etree.HTML(text)
    trs = html.xpath('//tr')
    if len(trs) < 1:
        return
    proxies = []
    for tr in trs[1:]:
        proxy = {}
        data = [x.strip() for x in tr.xpath('string(.)').strip().split('\n')]
        proxy['address'] = '{ip}:{port}'.format(ip=data[0], port=data[1])
        proxy['anonymity'] = data[2]
        proxy['type'] = data[3]
        proxy['position'] = data[4]
        proxies.append(proxy)
    deal_proxies(proxies)
    page += 1
    time.sleep(2)
    deal_kuaidaili_url(url, page=page)


def spider_kuaidaili():
    kuaidaili_urls = [
        'http://www.kuaidaili.com/free/inha/{0}',
        'http://www.kuaidaili.com/free/intr/{0}',
        'http://www.kuaidaili.com/free/outha/{0}',
        'http://www.kuaidaili.com/free/outtr/{0}',
    ]
    pool = Pool(4)
    pool.map(deal_kuaidaili_url, kuaidaili_urls)
    pool.close()
    pool.join()


def main():
    spider_kuaidaili()