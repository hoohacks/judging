from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register', views.register, name='register'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('profile', views.profile, name='profile'),
    path('evaluate', views.evaluate, name='evaluate'),
    path('statistics', views.statistics, name='statistics'),
    path('assign_demos', views.assign_demos, name='assign_demos'),
    path('assign_tables', views.assign_tables, name='assign_tables'),
    path('import_devpost', views.import_devpost, name='import_devpost'),
    path('edit_organizations', views.edit_organizations, name='edit_organizations'),
    path('add_organization', views.add_organization, name='add_organization'),
    path('delete_organization', views.delete_organization, name='delete_organization'),
    path('update_organization', views.update_organization, name='update_organization'),
    path('login', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout', auth_views.LogoutView.as_view(next_page='index'), name='logout'),
]