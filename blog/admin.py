from django.contrib import admin
from blog.models import Post, Category, Tag
# Register your models here.
class PostAdmin(admin.ModelAdmin):
    #列表展现的内容
    list_display = ['title', 'created_time','modified_time','category','author']
    #表单中需要填写的内容
    fields = ['title', 'content', 'abstract','category','tags']

    # 调用可以将博客作者直接设定为登录后台的用户
    def save_model(self, request, obj, form, change):
        obj.author = request.user
        super().save_model(request,obj,form,change)

admin.site.register(Post, PostAdmin)
admin.site.register(Category)
admin.site.register(Tag)
