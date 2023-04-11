from django.urls import path
from . import views

urlpatterns = [
    path(r'', views.index, name='index'),
    path(r'login/', views.login, name='login'),
    path(r'register/', views.register, name='register'),

    path(r'api/login/', views.api_login, name='api-login'),
    path(r'api/register/', views.api_register, name='api-register'),
    path(r'api/search/', views.api_search, name='api-search'),
    path(r'api/query/', views.QueryList.as_view(), name='api-query-list'),
    path(r'api/query/delete/', views.delete_query, name='api-query-delete'),
    path(r'api/article/', views.ArticleList.as_view(), name='api-article-list'),
    path(r'api/user/', views.UserList.as_view(), name='api-user-list'),
    path(r'api/all_users/', views.api_users, name='api-user-list'),
    
    path(r'api/test/', views.test, name='api-test'),
] 
