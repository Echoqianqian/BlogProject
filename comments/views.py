from django.shortcuts import render
from blog.models import Post
from django.shortcuts import  get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from .forms import CommentForm
from django.contrib import messages

def comment(request, post_pk):
    post = get_object_or_404(Post, pk = post_pk)
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.save()
        messages.add_message(request,messages.SUCCESS,'评论发表成功！',extra_tags='success')
        return redirect(post)
    context = {
        'post':post,
        'form':form,
    }
    messages.add_message(request, messages.ERROR,'评论发表失败，请重新修改错误再提交！',extra_tags='danger')
    return render(request, 'comments/preview.html',context=context)

