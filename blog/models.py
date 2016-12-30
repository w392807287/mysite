from django.db import models
import hashlib
from django.contrib.auth.models import AbstractUser

# Create your models here.


class Tag(models.Model):
    name = models.CharField('标签名', max_length=255)
    introduction = models.TextField('描述', default='为啥不给点描述呢', blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "标签"
        verbose_name_plural = "标签"


class Category(models.Model):
    name = models.CharField("分类名称", max_length=100)
    introduction = models.TextField('描述', default='为啥不给点描述呢', blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "分类"
        verbose_name_plural = "分类"


class Column(models.Model):
    name = models.CharField('专栏名称', max_length=100)
    introduction = models.TextField('描述', default='为啥不给点描述呢', blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "专栏"
        verbose_name_plural = "专栏"


class Author(models.Model):
    photo = models.ForeignKey('data.Image', verbose_name='头像', null=True, blank=True)
    name = models.CharField('用户名', max_length=255)
    followers = models.ManyToManyField('self', related_name='followees', symmetrical=False, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "作者"
        verbose_name_plural = "作者"


class Article(models.Model):
    title = models.CharField("文章标题", max_length=100)

    author = models.ForeignKey(Author, related_name='posts', verbose_name='作者')

    category = models.ManyToManyField(Category, verbose_name="文章分类", blank=True)
    tags = models.ManyToManyField(Tag, verbose_name='文章标签', blank=True)
    column = models.ForeignKey(Column, verbose_name='所属专栏', blank=True, null=True)

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




