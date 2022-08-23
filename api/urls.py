from django.urls import path
from . import views

urlpatterns = [
    path('', views.apiOverview, name='api-overview'),
    path('list/', views.postList, name='list'),
    path('view/<str:pk>/', views.postView, name='view'),
    path('create/', views.postCreate, name='create'),
    path('edit/<str:pk>/', views.postEdit, name='edit'),
    path('delete/<str:pk>/', views.postDelete, name='delete'),
]
