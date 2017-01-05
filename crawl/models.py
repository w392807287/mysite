from django.db import models
from mongoengine import *
import random
# from mysite.private_settings import M_DB_NAME, M_DB_HOST, M_DB_PORT

# connect(M_DB_NAME, host=M_DB_HOST, port=M_DB_PORT, connect=False)

# Create your models here.


# class BaseModel(Document):
#     create_at = DateTimeField()
#     meta = {
#         'allow_inheritance': True,
#         'abstract': True,
#     }


class Proxy(models.Model):
    address = models.CharField('代理地址', unique=True, max_length=255, blank=True)
    position = models.CharField('服务器地址', max_length=255, blank=True, default='')
    anonymity = models.CharField('匿名度', max_length=30, blank=True, default='')
    type = models.CharField('代理类型', blank=True, max_length=30, default='http')

    class Meta:
        verbose_name = "代理"
        verbose_name_plural = "代理"

    def __str__(self):
        return self.address

    @classmethod
    def get_random(cls):
        index = random.randint(0, cls.objects.all().count())
        return cls.objects.all()[index]


# class Proxy1(BaseModel):
#     address = StringField(db_field='address', name='代理地址', unique=True, max_length=100)
#     position = StringField(db_field='position', name='服务器地址', max_length=255, null=True, default='')
#     anonymity = StringField(db_field='anonymity', name='匿名度', max_length=255,)
#     type = StringField(db_field='type', name='类型', default='http')
#
#     meta = {'collection': 'proxy'}
#
#     def __str__(self):
#         return self.address
#
#     @classmethod
#     def get_random(cls):
#         # proxy = cls.objects.aggregate({'$sample': {'size': 1}}).next()
#         proxy = random.choice(cls.objects.all())
#         return proxy