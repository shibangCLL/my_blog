from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.http import HttpResponse
# from django.core.paginator import Paginator

from .models import Article, Carousel, Category, Tag, Comment,Course
from .forms import CommentForm

from utils.pagination import Pagination


def index(request):
    articles = Article.objects.all()[0:10]  # 默认首页显示最新5篇文章
    allcategory = Category.objects.all()
    carousels = Carousel.objects.all()
    articles_top = Article.objects.all().filter(is_top=True)
    context = {'articles': articles, 'carousels': carousels, 'articles_top': articles_top,
               'allcategory': allcategory}
    return render(request, 'blog/index.html', context)


def article_detail(request, slug):
    # 取出相应的文章
    article = Article.objects.get(slug=slug)
    article.update_views()
    article.body = article.body_to_markdown()
    comments = Comment.objects.filter(article=article)
    # 引入评论表单
    comment_form = CommentForm()
    cate = article.category
    post_list = Article.objects.filter(category=cate).order_by('-create_date')[0:8]

    # 需要传递给模板的对象
    context = {'article': article, 'comments': comments, 'comment_form': comment_form, 'post_list': post_list}
    # 载入模板，并返回context对象
    return render(request, 'blog/article_detail.html', context)


def category(request, slug):
    # 记得在开始部分导入 Category 类
    cate = get_object_or_404(Category, slug=slug)
    title = cate.name
    des = cate.description
    post_list = Article.objects.filter(category=cate).order_by('-create_date')
    page = Pagination(request, post_list.count(), 15)
    return render(request, 'blog/list.html',
                  context={'post_list': post_list[page.start:page.end], 'title': title, 'des': des,
                           'page_html': page.page_html})


def courses(request, slug):
    # 记得在开始部分导入 Category 类
    courses = get_object_or_404(Course, slug=slug)
    title = courses.name
    des = courses.description
    post_list = Article.objects.filter(course=courses).order_by('-create_date')
    page = Pagination(request, post_list.count(), 15)
    return render(request, 'blog/list.html',
                  context={'post_list': post_list[page.start:page.end], 'title': title, 'des': des,
                           'page_html': page.page_html})





def archive(request, year, month):
    post_list = Article.objects.filter(create_date__year=year,
                                       create_date__month=month,
                                       ).order_by('-create_date')
    title = str(year) + '年' + str(month) + '月文章'
    page = Pagination(request, post_list.count(), 15)
    return render(request, 'blog/list.html',
                  context={'post_list': post_list[page.start:page.end], 'title': title, 'page_html': page.page_html})


def tag(request, slug):
    # 记得在开始部分导入 Tag 类
    t = get_object_or_404(Tag, slug=slug)
    title = t.name
    des = t.description
    post_list = Article.objects.filter(tags=t).order_by('-create_date')
    page = Pagination(request, post_list.count(), 15)
    return render(request, 'blog/list.html',
                  context={'post_list': post_list[page.start:page.end], 'title': title, 'des': des,
                           'page_html': page.page_html})


def search(request):
    keyboard = request.GET.get('keyboard')

    if keyboard:
        post_list = Article.objects.filter(
            Q(title__icontains=keyboard) |
            Q(body__icontains=keyboard)
        )
    else:
        post_list = Article.objects.all()

    title = '包含' + keyboard + '的文章'
    des = keyboard
    page = Pagination(request, post_list.count(), 15)
    context = {'post_list': post_list[page.start:page.end], 'title': title, 'des': des, 'page_html': page.page_html}
    return render(request, 'blog/list.html', context)


# 时间轴
def time_line(request):
    articles = Article.objects.all()
    page = Pagination(request, articles.count(), 20)
    context = {'articles': articles[page.start:page.end], 'page_html': page.page_html}
    return render(request, 'blog/time-line.html', context)


def post_comment(request, article_id):
    """
    :param request:
    :param article_id: 文章id
    :return:
    """
    article = get_object_or_404(Article, id=article_id)
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.article = article
            new_comment.save()
            return redirect(article)
        else:
            return HttpResponse("表单内容有误，请重新填写。")
    else:
        return HttpResponse("发表评论仅接受POST请求。")


def increase_likes(request, id):
    """
    点赞
    :param request:
    :param article_id: 文章id
    :return:
    """
    if request.method == 'POST':
        article = Article.objects.get(id=id)
        article.likes += 1
        article.save()
        return HttpResponse('success')


def categories_list(request):
    cate_list = Category.objects.all()
    return render(request, 'blog/categories_list.html',
                  context={'cate_list': cate_list})


def courses_list(request):
    cate_list = Course.objects.all()
    return render(request, 'blog/courses_list.html',
                  context={'cate_list': cate_list})
