from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="news-home"),
    path('<str:cat>/', views.articles_by_category, name="category-articles"),
    path('article/<int:id>/', views.article_page, name="article-page"),
    path('addcomment', views.addcomment, name="addcomment"),
    path('editcomment', views.editComment, name="editcomment"),
    
]
