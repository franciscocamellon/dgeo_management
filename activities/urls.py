from django.urls import path
from . import views

urlpatterns = [
    path('', views.activities_list, name='activities_list')
]
