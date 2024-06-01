from django.urls import path
from .views import PostDetailView, PostList, PostCreate, PostUpdate, PostDelete, subscriptions
from django.views.decorators.cache import cache_page

urlpatterns = [
    path('', cache_page(60)(PostList.as_view()), name='post_list'),
    path('<int:pk>', cache_page(60)(PostDetailView.as_view()), name='post_detail'),
    path('news/create/', PostCreate.as_view(), name='news_create'),
    path('news/<int:pk>/update/', PostUpdate.as_view(), name='news_update'),
    path('news/<int:pk>/delete/', PostDelete.as_view(), name='news_delete'),

    path('articles/<int:pk>/delete/', PostDelete.as_view(), name='articles_delete'),
    path('articles/<int:pk>/update/', PostUpdate.as_view(), name='articles_update'),
    path('articles/create/', PostCreate.as_view(), name='articles_create'),
    path('subscriptions/', subscriptions, name='subscriptions'),
]
