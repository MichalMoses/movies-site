from django.urls import path
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

app_name='movies'

urlpatterns = [
    path('', views.movie_list, name='list'),
    path('create/', views.movie_create, name='create'),
    path('<slug:slug>/', views.movie_details, name='details'),
    path('<slug:slug>/addreview/', views.add_review, name='addreview')

]

urlpatterns += staticfiles_urlpatterns()
