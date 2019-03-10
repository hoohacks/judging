from django.urls import path

from . import views

app_name = 'api'
urlpatterns = [
    path('test', views.test_page, name="test_page"),
    path('user/create', views.user_create, name='user_create'),
    path('user/search', views.user_search, name='user_search'),
    path('user/update', views.user_update, name='user_update'),
    path('user/delete', views.user_delete, name='user_delete'),
]
