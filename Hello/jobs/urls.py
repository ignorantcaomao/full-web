from django.urls import path
from . import views

urlpatterns = [
    path('s/', views.async_celery, name='async_celery'),
    path('a/', views.apply_celery, name='apply_celery'),
]
