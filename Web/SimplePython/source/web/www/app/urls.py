from django.urls import path
from app import views
urlpatterns = [
    path('', views.index, name='index'),
    path('profile', views.profile, name='profile'),
    path('details', views.details, name='details'),
    path('logout', views.log_out, name='logout')
]