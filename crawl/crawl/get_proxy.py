from crawl.models import Proxy
from fake_useragent import UserAgent
from .util import TIMEOUT
import re
import random
import requests
from multiprocessing.dummy import Pool as ThreadPool
from mongoengine import connect
from multiprocessing import Pool as ProcessPool
import queue
from lxml import etree
import time
from mysite.private_settings import M_DB_NAME, M_DB_HOST, M_DB_PORT
from requests.exceptions import RequestException


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


def prove_proxy(proxy):
    try:
        _ = fetch('http://baidu.com', proxy=proxy.address)
        print('proxy {0} is ok....'.format(proxy.address))
    except Exception as e:
        print('proxy {0} make a error so was delete....'.format(proxy.address))
        proxy.delete()


def prove_proxies():
    # connect(M_DB_NAME, host=M_DB_HOST, port=M_DB_PORT, connect=False)
    proxies = Proxy.objects.all()
    pool = ThreadPool(8)
    pool.map(prove_proxy, proxies)
    pool.close()
    pool.join()


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


def deal_proxy(proxy):
    try:
        _ = fetch('http://baidu.com', proxy=proxy['address'])
        p = Proxy()
        for k, v in proxy.items():
            p.__setattr__(k, v)
        p.save()
        print('proxy {0} is ok....'.format(proxy['address']))
    except Exception as e:
        print('proxy {0} make a error so was delete....'.format(proxy['address']))


def deal_proxies(proxies):
    pool = ThreadPool(10)
    pool.map(deal_proxy, proxies)
    pool.close()
    pool.join()


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


def deal_xici_url(url):
    host = 'http://www.xicidaili.com'
    text = get_content_proxy(url).text
    html = etree.HTML(text)
    trs = html.xpath('//table[@id="ip_list"]/tr')[1:]
    if len(trs) < 5:
        return
    proxies = []
    for tr in trs:
        proxy = {}
        data = [x.strip() for x in tr.xpath('string(.)').strip().split('\n') if x.strip() != '']
        proxy['address'] = '{ip}:{port}'.format(ip=data[0], port=data[1])
        proxy['position'] = data[2]
        proxy['anonymity'] = data[3]
        proxy['type'] = data[4]
        proxies.append(proxy)
    deal_proxies(proxies)
    nextpage = html.xpath('//a[@class="next_page"]/@href')[0]
    url2 = host + nextpage
    deal_xici_url(url2)


def spider_kuaidaili():
    kuaidaili_urls = [
        'http://www.kuaidaili.com/free/inha/{0}',
        'http://www.kuaidaili.com/free/intr/{0}',
        'http://www.kuaidaili.com/free/outha/{0}',
        'http://www.kuaidaili.com/free/outtr/{0}',
    ]
    pool = ThreadPool(4)
    pool.map(deal_kuaidaili_url, kuaidaili_urls)
    pool.close()
    pool.join()


def spider_xici():
    xici_urls = [
        'http://www.xicidaili.com/nn/',
        'http://www.xicidaili.com/nt/',
        'http://www.xicidaili.com/wn/',
        'http://www.xicidaili.com/wt/',
    ]
    pool = ThreadPool(4)
    pool.map(deal_xici_url, xici_urls)
    pool.close()
    pool.join()


def main():
    # prove_proxies()
    # spider_kuaidaili()
    spider_xici()