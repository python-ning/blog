# coding:utf-8
import logging
from django.shortcuts import render, render_to_response, redirect
from django.conf import settings
from django.core.paginator import Paginator, InvalidPage, EmptyPage, PageNotAnInteger  # 分页器的类和一些异常的处理
from django.db import connection
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.hashers import make_password
from django.db.models import Count
from blog.models import *
from forms import *
from django import forms
# Create your views here.
# 业务逻辑的代码一般都在这里面

logger = logging.getLogger('blog.views')


def global_setting(request):
    # 站点基本信息
    SITE_NAME = settings.SITE_NAME
    SITE_DESC = settings.SITE_DESC
    WEIBO_TENGXUN = settings.WEIBO_TENGXUN
    E_MAIL = settings.E_MAIL
    # 分类信息获取（导航数据）
    category_list = Index.objects.all()
    # 文档归档数据
    archive_list = Article.objects.distinct_date()
    # 标签云数据
    tag_list = Tag.objects.all()
    # 友情链接数据
    links = Links.objects.all()
    # 文章排行榜的数据
    article_ranking_list = Article.objects.all().order_by('-click_count')
    # 评论排行
    comment_count_list = Comment.objects.values('article').annotate(
        comment_count=Count('article')).order_by('-comment_count')
    article_comment_list = [Article.objects.get(
        pk=comment['article'])for comment in comment_count_list]
    # 站长推荐
    sute_recommend_list = Article.objects.all().filter(is_recommend=1)
    return locals()


def index(request):
    try:
        article_list = getPage(request, Article.objects.all())
        # 文章归档
        # 获取文章的年份-月份 2015/06文章归档
        # print Article.objects.values('date_publish').distinct() 不可行
        # archive_list = Article.objects.raw('SELECT id, DATE_FORMAT(date_publish,"%%Y-%%m") as col_date FROM blog_article ORDER BY date_publish') 不可行
        # for i in archive_list:
        #     print i
        # cursor = connection.cursor()
        # cursor.execute("SELECT DISTINCT DATE_FORMAT(date_publish,'%Y-%m') as col_date FROM blog_article ORDER BY date_publish") 不推荐
        # row = cursor.fetchall()
        # print row
        archive_list = Article.objects.distinct_date()
        cate_list = Category.objects.all()

    except Exception as e:
        print e
        logger.error(e)
    return render(request, 'index.html', locals())


def archive(request):
    try:
        # 先获取客户端提交的信息
        year = request.GET.get('year', None)
        month = request.GET.get('month', None)
        article_list = Article.objects.filter(
            date_publish__icontains=year + '-' + month)
        article_list = getPage(request, article_list)
    except Exception as e:
        logger.error(e)
    return render(request, 'archive.html', locals())


# 分页代码
def getPage(request, article_list):
    paginator = Paginator(article_list, 4)
    try:
        page = int(request.GET.get('page', 1))
        article_list = paginator.page(page)
    except (EmptyPage, InvalidPage, PageNotAnInteger):
        article_list = paginator.page(1)
    return article_list


# 文章详情
def article(request):
    try:
        print 123235456687
        # 获取文章Id
        id = request.GET.get('id', None)
        try:
            # 获取文章信息
            article = Article.objects.get(pk=id)
            print article
        except Article.DoesNotExist:
            return render(request, 'failure.html', {'reason': '没有找到对应的文章'})

        # 评论表单
        comment_form = CommentForm({'author': request.user.username,
                                    'email': request.user.email,
                                    'url': request.user.url,
                                    'arctile': id} if request.user.is_authenticated() else{'arctile': id})
        comments = Comment.objects.filter(article=article).order_by('id')
        comment_list = []
        for comment in comments:
            for item in comment_list:
                if not hasattr(item, 'children_comment'):
                    setattr(item, 'children_comment', [])
                if comment.pid == item:
                    item.children_comment.append(comment)
                    break
            if comment.pid is None:
                comment_list.append(comment)
    except Exception as e:
        print e
        logger.error(e)
    return render(request, 'article.html', {"article":article})


# 提交评论
def comment_post(request):
    try:
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            # 获取表单信息
            comment = Comment.objects.create(username=comment_form.cleaned_data['author'],
                                             email=comment_form.cleaned_data[
                                                 'email'],
                                             url=comment_form.cleaned_data[
                                                 'url'],
                                             content=comment_form.cleaned_data[
                                                 'comment'],
                                             article_id=comment_form.cleaned_data[
                                                 'article'],
                                             user=request.user if request.user.is_authenticated() else None)
            comment.save()
        else:
            return render(request, 'failure.html', {'reason': comment_form.errors})
    except Exception as e:
        logger.error(e)
    return redirect(request.META['HTTP_REFERER'])


# 注销
def do_logout(request):
    try:
        logout(request)
    except Exception as e:
        print e
        logger.error(e)
    return redirect(request.META['HTTP_REFERER'])


# 注册
def do_reg(request):
    try:
        if request.method == 'POST':
            reg_form = RegForm(request.POST)
            if reg_form.is_valid():
                # 注册
                user = User.objects.create(username=reg_form.cleaned_data['username'],
                                           email=reg_form.cleaned_data[
                                               'email'],
                                           url=reg_form.cleaned_data['url'],
                                           password=make_password(reg_form.cleaned_data['password']),)
                user.save()
                # 登录
                user.backend = 'django.contrib.auth.backends.ModelBackend'  # 指定默认的登陆验证
                login(request, user)
                return redirect(request.POST.get('source_url'))
            else:
                return render(request, 'failure.html', {'reason': reg_form.errors})
        else:
            reg_form = RegForm()
    except Exception as e:
        logger.error(e)
    return render(request, 'reg.html', locals())


# 登录
def do_login(request):
    try:
        if request.method == 'POST':
            login_form = LoginForm(request.POST)
            if login_form.is_valid():
                # 登录
                username = login_form.cleaned_data['username']
                password = login_form.cleaned_data['username']
                user = authenticate(username=username, password=password)
                if user is not None:
                    user.backend = 'django.contrib.auth.backends.ModelBackend'  # 指定默认的登录
                    login(request, user)
                else:
                    return render(request, 'failure.html', {'reason': '登陆验证失败'})
                return redirect(request.POST.get('source_url'))
            else:
                return render(request, 'failure.html', {'reason': login_form.errors})
        else:
            login_form = LoginForm()
    except Exception as e:
        logger.error(e)
    return render(request, 'login.html', locals())


def articlelist(request):
    articles = Article.objects.all()
    return render(request, 'articlelist.html', locals())
