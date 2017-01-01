import requests
import json
import datetime
from data.models import AreaHousingPrice
from data.util.util import ALL_AREA_NAME_OF_SH


class SpiderLianjia(object):
    def __init__(self):
        self.formdata = {
            'access_token': '7poanTTBCymmgE0FOn1oKp',
            'client': 'pc',
            'cityCode': 'sh',
            'siteType': 'quyu',
            'type': 'district',
            'dataId': 'sh',
            'showType': 'list',
            'limit_offset': '0',
            'limit_count': '2000',
        }
        self.start_urls = [
            'http://soa.dooioo.com/api/v4/online/house/ershoufang/listMapResult',
        ]

    @staticmethod
    def get_url(url, *args, **kwargs):
        params = kwargs.get('params', None)
        try:
            content = requests.get(url, params=params).content
            content = str(content, encoding="utf8")
            return content
        except Exception as e:
            raise e

    def start(self):
        for url in self.start_urls:
            self.lianjia_junjia(url, formdata=self.formdata)

    def lianjia_junjia(self, url, formdata):
        content = self.get_url(url=url, params=formdata)
        data = json.loads(content)['dataList']
        for datum in data:
            self.dump_data(datum)
            if datum['currentType'] == 'district':
                formdata['dataId'] = datum['dataId']
                formdata['type'] = 'plate'
                self.lianjia_junjia(url, formdata)

    def dump_data(self, data):
        ahp = AreaHousingPrice()
        ahp.area_name = data.get('showName', '')
        ahp.dealAvgPrice = data.get('dealAvgPrice', '')
        ahp.saleAvgPrice = data.get('saleAvgPrice', '')
        ahp.total = data.get('saleTotal', '')
        ahp.saleType = '2'
        ahp.date = datetime.datetime.now().date()
        ahp.data_source = 'lianjia'
        ahp.save()


class FillData(object):
    def __init__(self, source, year, month, date):
        self.year = year
        self.month =month
        self.date = date
        self.source = source

    def fill(self):
        o_time = datetime.date(self.year, self.month, self.date)
        l_time = datetime.date(self.year, self.month, self.date - 1)
        n_time = datetime.date(self.year, self.month, self.date + 1)
        for area in ALL_AREA_NAME_OF_SH:
            try:
                print('processing....{0}'.format(area))
                ahp_o = AreaHousingPrice()
                ahp_l = AreaHousingPrice.objects.filter(area_name=area, date=l_time)[0]
                ahp_n = AreaHousingPrice.objects.filter(area_name=area, date=n_time)[0]
                ahp_o.area_name = area
                ahp_o.dealAvgPrice = int((ahp_l.dealAvgPrice + ahp_n.dealAvgPrice) / 2)
                ahp_o.saleAvgPrice = int((ahp_l.saleAvgPrice + ahp_n.saleAvgPrice) / 2)
                ahp_o.total = int((ahp_l.total + ahp_n.total) / 2)
                ahp_o.saleType = ahp_l.saleType
                ahp_o.data_source = self.source
                ahp_o.date = o_time
                ahp_o.save()
            except Exception as e:
                print(e)


def lianjia_junjia():
    spider = SpiderLianjia()
    spider.start()


def fill_data(source, year, month, date):
    fd = FillData(source, year, month, date)
    fd.fill()