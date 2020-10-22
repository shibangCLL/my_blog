from django.urls import path
from . import views

# 正在部署的应用的名称
app_name = 'blog'

urlpatterns = [
    path('search/', views.search, name='search'),
    path('time-line/', views.time_line, name='time_line'),
    path('increase-likes/<int:id>/', views.increase_likes, name='increase_likes'),
    path('categories_list/', views.categories_list, name='categories_list'),
    path('courses_list/', views.courses_list, name='courses_list'),
    path('', views.index, name='index'),
    path('<slug:slug>/', views.article_detail, name='article_detail'),
    path('categories/<slug:slug>/', views.category, name='category'),
    path('courses/<slug:slug>/', views.courses, name='courses'),
    path('archives/<int:year>/<int:month>/', views.archive, name='archive'),
    path('tags/<slug:slug>/', views.tag, name='tag'),
    path('post-comment/<int:article_id>/', views.post_comment, name='post_comment'),

]
