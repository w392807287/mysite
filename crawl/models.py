from django.db import models
from mongoengine import *
import random
from mysite.private_settings import M_DB_NAME, M_DB_HOST, M_DB_PORT

connect(M_DB_NAME, host=M_DB_HOST, port=M_DB_PORT, connect=False)

# Create your models here.


class BaseModel(Document):
    create_at = DateTimeField()
    meta = {
        'allow_inheritance': True,
        'abstract': True,
    }


class Proxy(BaseModel):
    address = StringField(db_field='address', name='代理地址', unique=True, max_length=100)
    position = StringField(db_field='position', name='服务器地址', max_length=255, null=True, default='')
    anonymity = StringField(db_field='anonymity', name='匿名度', max_length=255,)
    type = StringField(db_field='type', name='类型', default='http')

    meta = {'collection': 'proxy'}

    def __str__(self):
        return self.address

    @classmethod
    def get_random(cls):
        # proxy = cls.objects.aggregate({'$sample': {'size': 1}}).next()
        proxy = random.choice(cls.objects.all())
        return proxy