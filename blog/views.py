from django.shortcuts import render
from django.http import HttpResponse
from blog.models import Post,Category,Tag
from django.shortcuts import get_object_or_404
import markdown
import re
from django.utils.text import slugify
from markdown.extensions.toc import TocExtension


# Create your views here.
def index(request):
    post_list = Post.objects.all().order_by('-created_time')
    context = {'post_list' : post_list}
    return render(request, 'blog/index.html', context)

def detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    # post.content = markdown.markdown(post.content,
    #                                  extensions=[
    #                                      'markdown.extensions.extra',
    #                                      'markdown.extensions.codehilite',
    #                                      'markdown.extensions.toc',
    #                                  ])
    md = markdown.Markdown(extensions=[
        'markdown.extensions.extra',
        'markdown.extensions.codehilite',
        # 用于处理地址栏锚点显示
        TocExtension(slugify=slugify),
    ])
    post.content = md.convert(post.content)
    # 判断传递进去的文章标题是否为空，如果为空则不会创建文章标题目录，否则就会创建文章目录
    m = re.search(r'<div class="toc">\s*<ul>(.*)</ul>\s*</div>', md.toc, re.S)
    post.toc = m.group(1) if m is not None else ''
    return render(request, 'blog/detail.html',{'post' : post})

# 归档视图函数
def archive(request, year, month):
    post_list = Post.objects.filter(created_time__year=year,
                                    created_time__month=month).order_by('-created_time')
    return render(request,'blog/index.html',{'post_list':post_list})

# 分类视图函数
def category(request, pk):
    cate = get_object_or_404(Category, pk=pk)
    post_list = Post.objects.filter(category=cate).order_by('-created_time')
    return render(request, 'blog/index.html',{'post_list':post_list})

# 标签视图函数
def tag(request, pk):
    tag = get_object_or_404(Tag, pk = pk)
    post_list = Post.objects.filter(tags=tag).order_by('-created_time')
    return render(request, 'blog/index.html',{'post_list':post_list})