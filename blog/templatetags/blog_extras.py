from django import template
from ..models import Post, Category, Tag
register = template.Library()

# 显示最新文章
@register.inclusion_tag('blog/inclusions/_recent_posts.html', takes_context=True)
def show_recent_posts(context, num=5):
    return {
        'recent_post_list': Post.objects.all().order_by('-created_time')[:num],
    }

# 根据文章创建日期按照月份进行归档
@register.inclusion_tag('blog/inclusions/_archives.html', takes_context=True)
def show_archives(context):
    return {
        'date_list':Post.objects.dates('created_time','month', order='DESC'),
    }

# 给文章进行分类
@register.inclusion_tag('blog/inclusions/_categories.html', takes_context=True)
def show_categories(context):
    return {
        'category_list':Category.objects.all(),
    }

# 根据标签进行分类
@register.inclusion_tag('blog/inclusions/_tags.html', takes_context=True)
def show_tags(context):
    return {
        'tag_list':Tag.objects.all(),
    }
