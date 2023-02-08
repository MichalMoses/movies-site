from django.urls import path
from . import views
app_name='actors'

urlpatterns = [
    path('', views.actors_list, name='list'),
    path('<slug:slug>/', views.actor_details, name='details'),

]