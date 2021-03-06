from django.db import models
from entity.models import Area
from data.util.util import HOUSING_PRICE_SOURCE, HOUSING_PRICE_TYPE
import datetime
# Create your models here.


class Image(models.Model):
    title = models.CharField("图片名称", max_length=100, blank=True)
    image = models.ImageField("图片", upload_to='uploads/images/')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "图像"
        verbose_name_plural = "图像"


class File(models.Model):
    title = models.CharField("文件名称", max_length=100, blank=True)
    file = models.ImageField("文件", upload_to='uploads/images/')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "文件"
        verbose_name_plural = "文件"


class AreaHousingPrice(models.Model):
    area = models.ForeignKey('entity.Area', related_name='area_hosing_price', null=True)
    area_name = models.CharField('地区名', max_length=30, blank=True, default='', unique_for_date='date')  # 字段冗余，优化查询
    dealAvgPrice = models.FloatField('成交均价', null=True)
    saleAvgPrice = models.FloatField('挂牌均价', null=True)
    saleType = models.CharField('出售类型', max_length=255, choices=HOUSING_PRICE_TYPE, default='2')
    total = models.IntegerField('总共在售', default=0)
    date = models.DateField('日期', editable=True, null=True)
    data_source = models.CharField('数据来源', max_length=255, choices=HOUSING_PRICE_SOURCE, default='other')

    def __str__(self):
        return '%s - %s' % (self.area_name, self.date)

    def save(self, *args, **kwargs):
        if not self.date:
            self.date = datetime.datetime.now().strftime('%Y-%m-%d')

        super(AreaHousingPrice, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "地区房价"
        verbose_name_plural = "地区房价"
