from django.db import models
# Create your models here.

AREA_LEVEL = (
    ('0', '国家'),
    ('1', '省份/直辖'),
    ('2', '市'),
    ('3', '县/区'),
    ('4', '-'),
    ('5', '-'),
    ('6', '-'),
)


class Area(models.Model):
    name = models.CharField('地区名称', max_length=255, blank=True)
    level = models.CharField('行政等级', choices=AREA_LEVEL, default='6', max_length=30)
    code = models.CharField('行政代码', max_length=100, blank=True, default='000000000000')
    higher = models.ForeignKey('Area', verbose_name='行政上级', null=True)

    def __str__(self):
        return self.name
