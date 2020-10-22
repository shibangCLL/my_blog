from django import template

from ..models import Article, Category, Tag

register = template.Library()


@register.simple_tag
def keywords_to_str(art):
    '''将文章关键词变成字符串'''
    keys = art.keywords.all()
    return ','.join([key.name for key in keys])


# 最新文章
@register.inclusion_tag('blog/inclusions/_recent_posts.html', takes_context=True)
def show_recent_posts(context, num=5):
    return {
        'recent_post_list': Article.objects.all().order_by('-create_date')[:num],
    }


# 返回所有Tag
@register.inclusion_tag('blog/inclusions/_tags.html', takes_context=True)
def show_tags(context):
    return {
        'tag_list': Tag.objects.all(),
    }


# 通过年月归类文章
@register.inclusion_tag('blog/inclusions/_archives.html', takes_context=True)
def show_archives(context):
    return {
        'date_list': Article.objects.dates('create_date', 'month', order='DESC'),
    }


# 作者推荐
@register.inclusion_tag('blog/inclusions/_author_recommend.html', takes_context=True)
def show_author_recommend(context, num=5):
    return {
        'rauthor_recommend_list': Article.objects.all().filter(is_top=True).order_by('-create_date')[:num],
    }


# 热门文章
@register.inclusion_tag('blog/inclusions/_hot_article.html', takes_context=True)
def show_hot_article(context, num=5):
    return {
        'hot_article_list': Article.objects.all().order_by('-views')[:num],
    }


# 返回所有分类
@register.inclusion_tag('blog/inclusions/_categories.html', takes_context=True)
def show_categories(context, num=5):
    return {
        'category_list': Category.objects.all(),
    }


# 返回所有分类 Banner列表
@register.inclusion_tag('blog/inclusions/_categories_banner.html', takes_context=True)
def show_categories_banner(context, num=5):
    return {
        'category_list': Category.objects.all(),
    }


# 分页
@register.inclusion_tag('blog/inclusions/_fenye.html', takes_context=True)
def list_fenye(context, num=5):
    return {
        'category_list': Category.objects.all(),
    }
