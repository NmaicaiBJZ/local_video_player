from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('play/<str:filename>/', views.play_video, name='play_video'),
]
