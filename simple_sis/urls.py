from django.urls import path
from .views import home, login, logout, view_activity

urlpatterns = [
    path('login', login, name='login'),
    path('logout', logout, name='logout'),
    path('', home, name='home'),
    path('activities/<int:id>', view_activity, name='view-activity'),
]
