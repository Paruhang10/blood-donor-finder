from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('toggle/', views.toggle, name='toggle'),
    path('search/', views.search, name='search'),
    path('request/<int:donor_id>/', views.submit_request, name='request'),
    path('request-sent/', views.request_sent, name='request_sent'),
]