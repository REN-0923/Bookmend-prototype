from django.urls import path

from . import views

urlpatterns = [
    path('', views.create, name='create'),
    path('statistic', views.statistic, name='statistic'),
    path('description/<int:pk>', views.description, name='description'),
]