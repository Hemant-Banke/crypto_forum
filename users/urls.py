from django.urls import path, include
from . import views

app_name = 'users'

urlpatterns = [
    path('registration', views.registration, name='registration'),
    path('login', views.login, name="login"),
    path('logout', views.logout, name="logout"),

    path('profile/<str:username>', views.profile, name="profile"),
]
