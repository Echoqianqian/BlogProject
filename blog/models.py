from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from django.utils.html import strip_tags
import markdown
# Create your models here.

class Category(models.Model):
    '''blog category'''
    #name - category name
    cat_name = models.CharField(max_length=100)

    class Meta:
        verbose_name = '分类'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.cat_name

class Tag(models.Model):
    '''blog tag'''
    #name --tag name
    tag_name = models.CharField(max_length=100)
    class Meta:
        verbose_name = '标签'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.tag_name

class Post(models.Model):
    '''blog post'''
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_time = models.DateTimeField(default=timezone.now())
    modified_time = models.DateTimeField()
    abstract = models.CharField(max_length=200, blank=True)

    #blog's category and tags
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, blank=True)
    #blog's author
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    #用于确定用户建立新博客的时候最后的修改时间能是调用这个模型自动获取的时间
    def save(self,*args,**kwargs):
        self.modified_time = timezone.now()
        # 从文章内容中自动摘取前54个字符作为文章摘要，需要将Markdown格式转换为HTML，然后再取字符
        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
        ])
        self.abstract = strip_tags(md.convert(self.content))[:54]
        super().save(*args,**kwargs)
    class Meta:
        verbose_name = '文章'
        verbose_name_plural = verbose_name
        ordering = ['-created_time'] #根据创建时间逆序来排序

    # 自动寻找detail视图函数，并且将参数传递过去，然后根据URL规则，将相应的结果传递给detail对应的HTML文件中进行显示
    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.title
