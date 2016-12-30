from django.db import models
from django.contrib.auth.models import AbstractUser
from .util.util import SimHash
import jieba.analyse
# Create your models here.


class Tag(models.Model):
    name = models.CharField('标签名', max_length=255, unique=True)
    introduction = models.TextField('描述', default='为啥不给点描述呢', blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "标签"
        verbose_name_plural = "标签"


class Category(models.Model):
    name = models.CharField("分类名称", max_length=100, unique=True)
    introduction = models.TextField('描述', default='为啥不给点描述呢', blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "分类"
        verbose_name_plural = "分类"


class Column(models.Model):
    name = models.CharField('专栏名称', max_length=100, unique=True)
    introduction = models.TextField('描述', default='为啥不给点描述呢', blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "专栏"
        verbose_name_plural = "专栏"


class Author(models.Model):
    photo = models.ImageField('用户头像', blank=True, null=True, upload_to='uploads/images/heads/')
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

    simhash_code = models.CharField('sim哈希', max_length=64, blank=True, null=True)

    category = models.CharField(verbose_name="文章分类", blank=True, max_length=255, default='')
    tags = models.CharField(verbose_name='文章标签', blank=True, max_length=255, default='')
    column = models.ForeignKey(Column, verbose_name='所属专栏', blank=True, null=True)

    pub_date = models.DateTimeField("发布日期", auto_now_add=True, editable=True)
    update_time = models.DateTimeField("更新时间", auto_now=True, null=True)

    keywords = models.CharField("文章关键词", blank=True, max_length=255)
    summary = models.TextField("文章简介", blank=True, default="这鬼作者忘了写简介")
    content = models.TextField("文章正文", default='', blank=True)

    def save(self, _set=True, *args, **kwargs):
        if _set:
            self.set_sim_hash()
            self.set_keywords()
        super(Article, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    def set_keywords(self, top=20, withWeight=True):
        rank = jieba.analyse.textrank(self.content, topK=top, withWeight=withWeight)
        res = [x[0] for x in rank if x[1] > 0.5]
        self.keywords = ','.join(res)

    def set_sim_hash(self):
        self.simhash_code = SimHash.simhash(self.content)

    class Meta:
        ordering = ['-pub_date']
        verbose_name = "文章"
        verbose_name_plural = "文章"




