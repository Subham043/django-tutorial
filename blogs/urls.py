from django.urls import path

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
]