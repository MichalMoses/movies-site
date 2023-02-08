from django.contrib import admin
from django.urls import path
from . import views
import movies_site

app_name='accounts'

urlpatterns = [
    path('login/', views.login_view, name="login"),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('<slug:nonexist>/', movies_site.views.not_found, name='404')
]