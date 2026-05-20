from django.urls import path
from django.contrib.auth import views as auth_views
from .views import CustomLoginView, logout_view

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
]
