from django.urls import path
from . import views

app_name = 'blog'
urlpatterns = [
    # path(访问的网址+传递的参数， 视图函数，视图函数别名)
    # name 是前面views.index视图函数的别名
    path('', views.index, name='index'),
    path('posts/<int:pk>/',views.detail, name='detail'),
    path('archives/<int:year>/<int:month>/',views.archive, name='archives'),
    path('categories/<int:pk>/',views.category, name='category'),
    path('tags/<int:pk>/', views.tag,name='tag')
]