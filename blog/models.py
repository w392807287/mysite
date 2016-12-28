from django.db import models
import hashlib
from django.contrib.auth.models import AbstractUser

# Create your models here.


class Author(models.Model):
    photo = models.ForeignKey('data.Image', verbose_name='头像', null=True)
    username = models.CharField('用户名', max_length=255)
    followers = models.ManyToManyField('self', related_name='followees', symmetrical=False)


class Article(models.Model):
    title = models.CharField("博客标题", max_length=100)
    author = models.ForeignKey(Author, related_name='posts', verbose_name='作者')
    category = models.CharField("博客标签", max_length=100, blank=True)
    pub_date = models.DateTimeField("发布日期", auto_now_add=True, editable=True)
    update_time = models.DateTimeField("更新时间", auto_now=True, null=True)
    summary = models.TextField("文章简介", blank=True, default="这鬼作者忘了写简介")
    content = models.TextField("文章正文", default='', blank=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-pub_date']
        verbose_name = "文章"
        verbose_name_plural = "文章"


class Category(models.Model):
    name = models.CharField("标签名", max_length=100)


