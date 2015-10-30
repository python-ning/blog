# coding:utf-8
from django.contrib import admin
from models import *
# Register your models here.


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'desc', 'click_count',)
    # 这个可以显示到每个项目的标题处显示出来
    #list_display_links = ('title', 'desc', )
    # 把list_display的显示项目设置为可点击，点击了跳到该项目
    #fields = ('title', 'desc', 'content',)
    # 选择后台默认显示项
    #exclude = ('title', 'desc', 'content',)
    # 除了这些标签其他都显示
    list_editable = ('click_count',)
    # 显示在标题的项目可修改，这里是点击次数设置为了可修改
    #fieldsets = (
    #    (None, {
    #        'fields': ('title', 'desc', 'content', )
    #    }),
    #    ('高级设置', {
    #        'classes': ('collapse',),
    #        'fields': ('click_count', 'is_recommend', )
    #    }),
    #)
    # 可以将一些选项隐藏到一个标题这里是高级设置中，点开标题才能设置里边的内容
    #list_filter = ('title')
    # 哪些列可以被检索过滤

    class Media:
        js = (
            '/static/js/kindeditor-4.1.10/kindeditor-min.js',
            '/static/js/kindeditor-4.1.10/lang/zh_CN.js',
            '/static/js/kindeditor-4.1.10/config.js',
        )


class IndexAdmin(admin.ModelAdmin):
    list_display = ('name', 'index')


class CategoryAdmin(admin.ModelAdmin):
    fields = ('name', 'desc', 'pid', 'start')

admin.site.register(User)
admin.site.register(Tag)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Index, IndexAdmin)
admin.site.register(Comment)
admin.site.register(Links)
admin.site.register(Category, CategoryAdmin)
