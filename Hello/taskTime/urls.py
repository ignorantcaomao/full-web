from django.urls import path
from . import views
urlpatterns = [
    path('work/', views.workInfo, name='workitems'),
    path('insert/', views.test, name='test')
]
