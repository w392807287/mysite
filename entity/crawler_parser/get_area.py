# import requests
# from lxml import etree
# from entity.models import Area
# from entity.util.util import PROVINCE_CODE
# import datetime
#
# def main():
#     base_url = 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2015/{0}'
#     origin_url = base_url.format('index.html')
#
#     def deal_government(government):
#         name = government.get('name')
#         higher = government.get('hierarchy')
#         code = government.get('code')
#         level = len(higher.split('.'))
#         aa = Area.objects.filter(name=name, code=code, higher=higher)
#         if aa:
#             aa = aa[0]
#         else:
#             aa = Area()
#         aa.name = name
#         aa.higher = higher
#         aa.code = code
#         aa.level = level
#         try:
#             aa.save()
#         except:
#             print('save {0} - {1} error...'.format(higher, name))
#
#     def get_government_from_baike(name, code, hierarchy, lower):
#         # url = base_baike.format(name)
#         # content = requests.get(url).content
#         government = {
#             'name': name,
#             # 'content': content,
#             'hierarchy': hierarchy,
#             'code': code,
#             'lower': lower,
#         }
#         deal_government(government)
#
#     def get_selector(url):
#         content = requests.get(url).content
#         selector = etree.HTML(content)
#         return selector
#
#     def get_province(url):
#         selector = get_selector(url)
#         aa = selector.xpath('//tr[@class="provincetr"]/td/a')
#         hierarchy = '中国'
#         for a in aa:
#             name = a.xpath('text()')[0]
#             pre = hierarchy + '.' + name
#             code = PROVINCE_CODE.get(name, '000000000000')
#             url = base_url.format(a.xpath('@href')[0])
#             # get_government_from_baike(name, code, hierarchy)
#             yield get_city(
#                 url=url,
#                 hierarchy=pre,
#                 atom=(name, code, hierarchy),
#             )
#
#     def get_city(url, hierarchy, atom):
#         selector = get_selector(url)
#         trs = selector.xpath('//tr[@class="citytr"]')
#         lower = []
#         for tr in trs:
#             try:
#                 code = tr.xpath('td/a/text()')[0]
#                 name = tr.xpath('td/a/text()')[1]
#                 lower.append(name)
#                 url = base_url.format(tr.xpath('td/a/@href')[0])
#                 pre = hierarchy + '.' + name
#                 # get_government_from_baike(name, code, hierarchy)
#                 yield get_county(
#                     url=url,
#                     hierarchy=pre,
#                     atom=(name, code, hierarchy),
#                 )
#             except:
#                 continue
#         get_government_from_baike(
#             name=atom[0],
#             code=atom[1],
#             hierarchy=atom[2],
#             lower=lower,
#         )
#
#     def get_county(url, hierarchy, atom):
#         selector = get_selector(url)
#         trs = selector.xpath('//tr[@class="countytr"]')
#         lower = []
#         for tr in trs:
#             try:
#                 code = tr.xpath('td/a/text()')[0]
#                 name = tr.xpath('td/a/text()')[1]
#                 lower.append(name)
#                 # pre = hierarchy + '.' + name
#                 get_government_from_baike(name, code, hierarchy, [])
#             except:
#                 continue
#         get_government_from_baike(
#             name=atom[0],
#             code=atom[1],
#             hierarchy=atom[2],
#             lower=lower,
#         )
#
#     def get_town(url, hierarchy, atom):
#
#
#     def start():
#         for i in get_province(origin_url):
#             for j in i:
#                 j
#     start()