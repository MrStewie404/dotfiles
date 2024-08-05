from django.urls import path, include
from django.views.decorators.cache import cache_page

from .views import (
      PostsList, PostDetail,                  
      SearchList, NewsCreate,                  
      ArticleCreate, PostEdit, 
      PostDelete, subscriptions,
      CategoryList, Index,
   )


urlpatterns = [
   path('', cache_page(60)(PostsList.as_view()), name='posts_list'),
   path('search/', SearchList.as_view(), name='search_list'),
   path('search/<int:pk>', PostDetail.as_view(), name='search_detail'),
   path('<int:pk>', cache_page(60*5)(PostDetail.as_view()), name='post_detail'),
   path('<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),

   path('create/news/', NewsCreate.as_view(), name='news_create'),
   path('news/<int:pk>/edit/', PostEdit.as_view(), name='post_edit'),
   path('news/<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),

   path('create/article/', ArticleCreate.as_view(), name='article_create'),
   path('article/<int:pk>/edit/', PostEdit.as_view(), name='post_edit'),
   path('article/<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),


   path('categories/<int:pk>', CategoryList.as_view(), name='category_list'),
   path('subscriptions/', subscriptions, name='subscriptions'),

   path('test/', Index.as_view(), name='test'),
]


