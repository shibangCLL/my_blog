from django.contrib import admin

# Register your models here.
from .models import Article, Category, Tag, Keyword, Carousel, Comment, Course


class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'create_date', 'update_date', 'views', 'category']
    fields = ['title', 'summary', 'body', 'image', 'is_top', 'category', 'tags', 'keywords', 'course']

    def save_model(self, request, obj, form, change):
        obj.author = request.user
        super().save_model(request, obj, form, change)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    fields = ['name', 'description']


class CourseAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    fields = ['name', 'description']


class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    fields = ['name', 'description']


# 注册ArticlePost到admin中
admin.site.register(Article, ArticleAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Keyword)
admin.site.register(Carousel)
admin.site.register(Comment)
