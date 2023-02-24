from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from . import views

app_name = 'blogs'
urlpatterns = [
    path('test/', views.MorningGreetingView.as_view(), name='test'),
    path('form/', views.FormView.as_view(), name='form'),
    path('change-greeting/', views.GreetingView.as_view(greeting="G'day")),
    path('temp-view/', views.TempView.as_view(), name='temp_view'),
    path('article-list-view/', views.ArticleListView.as_view(), name='article_list_view'),
    path('article-detail-view/<int:pk>/', views.ArticleDetailView.as_view(), name='article_detail_view'),
    path('article/add/', views.ArticleCreateView.as_view(), name='article_add'),
    path('article/csv/', views.csv_view, name='article_csv'),
    path('article/<int:pk>/', views.ArticleUpdateView.as_view(), name='article_update'),
    path('article/<int:pk>/delete/', views.ArticleDeleteView.as_view(), name='article_delete'),
    
    #rest framework url
    path('articles-rest/', views.article_list),
    path('articles-rest/<int:pk>/', views.article_detail),
    path('articles-class-rest/', views.ArticleList.as_view()),
    path('articles-class-rest/<int:pk>/', views.ArticleDetail.as_view()),
    path('articles-class-mixin-rest/', views.ArticleMixinList.as_view()),
    path('articles-class-mixin-rest/<int:pk>/', views.ArticleMixinDetail.as_view()),
    path('articles-generic-rest/', views.ArticleGenericList.as_view()),
    path('articles-generic-rest/<int:pk>/', views.ArticleGenericDetail.as_view()),
    path('users-rest/', views.UserList.as_view()),
    path('users-rest/<int:pk>/', views.UserDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)