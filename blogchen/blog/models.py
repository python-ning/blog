# coding:utf-8
from django.contrib.auth.models import AbstractUser

# Create your models here.

# 用户模型
# 第一种：采用的继承方式扩展用户信息（本系统采用）
# 扩展：关联的方式去扩展用户信息

from django.db import models


# 用户
class User(AbstractUser):
    avatar = models.ImageField(
        upload_to='avatar/%Y/%m', default='avatar/default.png', max_length=200, verbose_name='头像')
    qq = models.CharField(max_length=20, blank=True,
                          null=True, unique=True, verbose_name='QQ号码')
    mobile = models.CharField(
        max_length=11, blank=True, null=True, unique=True, verbose_name='手机号码')
    url = models.URLField(max_length=100, blank=True,
                          null=True, verbose_name='个人网页地址')
    # 可以为空，不能重复

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = verbose_name
        ordering = ['-id']

    def __unicode__(self):
        return self.username


# tag(标签)
class Tag(models.Model):
    name = models.CharField(max_length=30, verbose_name='标签名称')

    class Meta:
        verbose_name = '标签'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name


# 文章导航
class Index(models.Model):
    name = models.CharField(max_length=30, verbose_name='导航名称')
    index = models.IntegerField(default=999, verbose_name='导航的排序')

    class Meta:
        verbose_name = '导航'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name


# 自定义一个文章Model的管理器
# 1.新加一个数据处理的方法
# 2.改变原有的Queryset
class ArticleManager(models.Manager):

    def distinct_date(self):
        distinct_date_list = []
        date_list = self.values('date_publish')
        for date in date_list:
            date = date['date_publish'].strftime('%Y/%m文章存档')
            if date not in distinct_date_list:
                distinct_date_list.append(date)
        return distinct_date_list


# 文章模型
class Article(models.Model):
    title = models.CharField(max_length=50, verbose_name='文章标题')
    desc = models.CharField(max_length=50, verbose_name='文章描述')
    content = models.TextField(verbose_name='文章内容')
    click_count = models.IntegerField(default=0, verbose_name='点击次数')
    is_recommend = models.BooleanField(default=1, verbose_name='是否推荐')
    date_publish = models.DateTimeField(auto_now_add=True, verbose_name='发布时间')
    user = models.ForeignKey(User, verbose_name='用户')
    category = models.ForeignKey(
        Index, blank=True, null=True, verbose_name='分类')
    tag = models.ManyToManyField(Tag, verbose_name='标签')

    objects = ArticleManager()

    class Meta:
        verbose_name = '文章'
        verbose_name_plural = verbose_name
        ordering = ['-date_publish']

    def __unicode__(self):
        return self.title


# 评论模型
class Comment(models.Model):
    content = models.TextField(verbose_name='评论的内容')
    username = models.CharField(
        max_length=30, blank=True, null=True, verbose_name='用户名')
    email = models.EmailField(
        max_length=50, blank=True, null=True, verbose_name='邮箱地址')
    url = models.URLField(max_length=100, blank=True,
                          null=True, verbose_name='个人网页地址')
    date_publish = models.DateTimeField(auto_now_add=True, verbose_name='发布时间')
    user = models.ForeignKey(User, blank=True, null=True, verbose_name='用户')
    article = models.ForeignKey(
        Article, blank=True, null=True, verbose_name='文章')
    pid = models.ForeignKey('self', blank=True, null=True, verbose_name='父级评论')

    class Meta:
        verbose_name = '评论'
        verbose_name_plural = verbose_name
        ordering = ['-date_publish']

    def __unicode__(self):
        return str(self.id)


# 友情链接
class Links(models.Model):
    title = models.CharField(max_length=50, verbose_name='标题')
    description = models.CharField(max_length=200, verbose_name='友情链接描述')
    callback_url = models.URLField(verbose_name='url地址')
    date_publish = models.DateTimeField(auto_now_add=True, verbose_name='发布时间')
    index = models.IntegerField(default=999, verbose_name='排列顺序（从小到大）')

    class Meta:
        verbose_name = '友情链接'
        verbose_name_plural = verbose_name
        ordering = ['index', 'id']

    def __unicode__(self):
        return self.title


# 广告
class Ad(models.Model):
    title = models.CharField(max_length=50, verbose_name='广告标题')
    description = models.CharField(max_length=200, verbose_name='广告描述')
    image_url = models.ImageField(upload_to='ad/%Y/%m', verbose_name='图片路径')
    callback_url = models.URLField(null=True, blank=True, verbose_name='回调url')
    date_publish = models.DateTimeField(auto_now_add=True, verbose_name='发布时间')
    index = models.IntegerField(default=999, verbose_name='排列顺序（从小到大）')

    class Meta:
        verbose_name = u'广告'
        verbose_name_plural = verbose_name
        ordering = ['index', 'id']

    def __unicode__(self):
        return self.title


class Category(models.Model):
    name = models.CharField(max_length=30, verbose_name='分类名')
    desc = models.CharField(max_length=50, blank=True,
                            null=True, verbose_name='分类描述')
    pid = models.ForeignKey('self', verbose_name='父级', blank=True, null=True)
    path = models.CharField(
        max_length=80, verbose_name='路径', blank=True, null=True)
    level = models.IntegerField(
        verbose_name='等级', default=0, blank=True, null=True)
    start = models.SmallIntegerField(
        choices=((0, '启动'), (1, '不启动')), default=0, verbose_name='是否启动')

    def save(self, *args, **kwargs):
        super(self.__class__, self).save(*args, ** kwargs)
        if self.pid is None:
            self.pid = 0
            self.level = 0
            self.path = 0
        else:
            self.level = self.pid.level + 1
            self.pid.id = self.id
            self.path = str(self.pid.id) + '--' + str(self.id)

        super(self.__class__, self).save(*args, ** kwargs)

    class Meta:
        verbose_name = u'分类'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name
