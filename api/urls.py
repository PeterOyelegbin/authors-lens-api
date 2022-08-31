from django.urls import path
from . import views

urlpatterns = [
    path('', views.apiOverview, name='api-overview'),
    path('signup/', views.signUp, name='signup'),
    path('login/', views.logIn, name='login'),
    path('logout/', views.logOut, name='logout'),
    path('list/', views.postList, name='list'),
    path('view/<str:pk>/', views.postView, name='view'),
    path('create/', views.PostCreate.as_view(), name='create'),
    path('edit/<str:pk>/', views.PostEdit.as_view(), name='edit'),
    path('delete/<str:pk>/', views.postDelete, name='delete'),
]
