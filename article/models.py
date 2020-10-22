import re
import os
import uuid

import markdown
from mdeditor.fields import MDTextField
from uuslug import slugify

from django.urls import reverse

from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField


def articleimage_directory_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = '{}.{}'.format(uuid.uuid4().hex[:10], ext)
    return os.path.join("articleimage", filename)


# 文章关键字
class Keyword(models.Model):
    name = models.CharField('文章关键词', max_length=20)

    class Meta:
        verbose_name = '关键词'
        verbose_name_plural = verbose_name
        ordering = ['name']

    def __str__(self):
        return self.name


# 文章标签
class Tag(models.Model):
    name = models.CharField('文章标签', max_length=20)
    slug = models.SlugField(unique=True)
    description = models.TextField('描述', max_length=240,
                                   help_text='用来作为SEO中description,长度参考SEO标准')

    def save(self, *args, **kwargs):
        if not self.id or not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = '标签'
        verbose_name_plural = verbose_name
        ordering = ['id']

    def __str__(self):
        return self.name


# 文章分类
class Category(models.Model):
    name = models.CharField('文章分类', max_length=20)
    slug = models.SlugField(unique=True)
    description = models.TextField('描述', max_length=240,
                                   help_text='用来作为SEO中description,长度参考SEO标准')

    def save(self, *args, **kwargs):
        if not self.id or not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = '分类'
        verbose_name_plural = verbose_name
        ordering = ['name']

    def __str__(self):
        return self.name


# 教程
class Course(models.Model):
    name = models.CharField('教程', max_length=20)
    slug = models.SlugField(unique=True)
    description = models.TextField('描述', max_length=240,
                                   help_text='用来作为SEO中description,长度参考SEO标准')

    def save(self, *args, **kwargs):
        if not self.id or not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = '教程'
        verbose_name_plural = verbose_name
        ordering = ['name']

    def __str__(self):
        return self.name


# 文章
class Article(models.Model):
    # IMG_LINK = '/static/blog/img/summary.png'
    author = models.ForeignKey(User, verbose_name='作者', on_delete=models.CASCADE)
    title = models.CharField(max_length=150, verbose_name='文章标题')
    slug = models.SlugField(max_length=250, unique=True)
    summary = models.TextField('文章摘要', max_length=230, default='文章摘要等同于网页description内容，请务必填写...')
    body = MDTextField(verbose_name='文章内容')
    image = models.ImageField('图片', upload_to=articleimage_directory_path)
    create_date = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    update_date = models.DateTimeField(verbose_name='修改时间', auto_now=True)
    views = models.IntegerField('阅览量', default=0)
    # 新增点赞数统计
    likes = models.PositiveIntegerField(default=0)

    is_top = models.BooleanField('置顶', default=False)

    category = models.ForeignKey(Category, verbose_name='文章分类', on_delete=models.PROTECT)
    course = models.ForeignKey(Course, verbose_name='课程', on_delete=models.PROTECT, blank=True, null=True)
    tags = models.ManyToManyField(Tag, verbose_name='标签')
    keywords = models.ManyToManyField(Keyword, verbose_name='文章关键词',
                                      help_text='文章关键词，用来作为SEO中keywords，最好使用长尾词，3-4个足够')

    def save(self, *args, **kwargs):
        if not self.id or not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = '文章'
        verbose_name_plural = verbose_name
        ordering = ['-create_date']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:article_detail', kwargs={'slug': self.slug})

    def body_to_markdown(self):
        return markdown.markdown(self.body, extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
        ])

    def update_views(self):
        self.views += 1
        self.save(update_fields=['views'])

    def get_pre(self):
        return Article.objects.filter(id__lt=self.id).order_by('-id').first()

    def get_next(self):
        return Article.objects.filter(id__gt=self.id).order_by('id').first()


# 幻灯片
class Carousel(models.Model):
    number = models.IntegerField('编号', help_text='编号决定图片播放的顺序，图片不要多于5张')
    title = models.CharField('标题', max_length=20, blank=True, null=True, help_text='标题可以为空')
    content = models.CharField('描述', max_length=80)
    image = models.ImageField('轮播图', upload_to='banner/%Y%m')
    # img_url = models.CharField('图片地址', max_length=200)
    url = models.CharField('跳转链接', max_length=256, default='#', help_text='图片跳转的超链接，默认#表示不跳转')

    class Meta:
        verbose_name = '图片轮播'
        verbose_name_plural = verbose_name
        # 编号越小越靠前，添加的时间约晚约靠前
        ordering = ['number', '-id']

    def __str__(self):
        return self.content[:25]


# 评论
class Comment(models.Model):
    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
        verbose_name='文章评论'
    )
    body = RichTextField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return self.body[:20]
