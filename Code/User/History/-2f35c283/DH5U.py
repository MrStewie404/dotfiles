from django.urls import path, include

from .views import (
      PostsList, PostDetail,                  
      SearchList, NewsCreate,                  
      ArticleCreate, PostEdit, 
      PostDelete, subscriptions
   )


urlpatterns = [
   path('', PostsList.as_view(), name='posts_list'),
   path('search/', SearchList.as_view(), name='search_list'),
   path('search/<int:pk>', PostDetail.as_view(), name='search_detail'),
   path('<int:pk>', PostDetail.as_view(), name='post_detail'),
   path('<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),

   path('create/news/', NewsCreate.as_view(), name='news_create'),
   path('news/<int:pk>/edit/', PostEdit.as_view(), name='post_edit'),
   path('news/<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),

   path('create/article/', ArticleCreate.as_view(), name='article_create'),
   path('article/<int:pk>/edit/', PostEdit.as_view(), name='post_edit'),
   path('article/<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),

   path('subscriptions/', subscriptions, name='subscriptions'),
]