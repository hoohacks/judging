from django.conf import settings
from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

urlpatterns = [
    # Judge
    path('', views.index, name='index'),
    path('register', views.register, name='register'),
    path('queue', views.queue, name='queue'),
    path('profile', views.profile, name='profile'),
    path('evaluate', views.evaluate, name='evaluate'),
    # Admin
    path('prejudging', views.prejudging, name='prejudging'),
    path('statistics', views.statistics, name='statistics'),
    path('scores', views.scores, name='scores'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('edit_event', views.edit_event, name='edit_event'),
    path('assign_demos', views.assign_demos, name='assign_demos'),
    path('assign_tables', views.assign_tables, name='assign_tables'),
    path('import_devpost', views.import_devpost, name='import_devpost'),
    # Services - categories
    path('import_categories_from_devpost', views.import_categories_from_devpost, name='import_categories_from_devpost'),
    path('edit_categories', views.edit_categories, name='edit_categories'),
    path('add_category', views.add_category, name='add_category'),
    path('delete_category', views.delete_category, name='delete_category'),
    path('update_category', views.update_category, name='update_category'),
    # Services - organizations
    path('add_organization', views.add_organization, name='add_organization'),
    path('delete_organization', views.delete_organization, name='delete_organization'),
    path('update_organization', views.update_organization, name='update_organization'),
    path('get_scores', views.get_scores, name='get_scores'),
    path('login', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout', auth_views.LogoutView.as_view(next_page='index'), name='logout'),
]

# DEVELOPMENT ONLY
if settings.DEBUG:
    urlpatterns += [
        path('generate_judges', views.generate_judges, name='generate_judges'),
        path('simulate_demos', views.simulate_demos, name='simulate_demos'),
    ]