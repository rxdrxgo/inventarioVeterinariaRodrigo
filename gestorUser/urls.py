from django.contrib import admin
from django.urls import path, include
from . import views
from .views import SignUpView

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('profile/', views.verProfile, name='profile'),
    path('profile_edit/', views.profile_edit, name='profile_edit')
]
