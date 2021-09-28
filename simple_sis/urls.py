from django.urls import path
from .views import home, login, logout

urlpatterns = [
    path('login', login, name='login'),
    path('logout', logout, name='logout'),
    path('', home, name='home'),
]
