from django.urls import path
from . import views

urlpatterns = [
    # path('work/', views.workInfo, name='workitems'),
    path('workitems/', views.WorkItemsView.as_view(), name='workitems'),
]
