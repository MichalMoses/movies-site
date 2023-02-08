from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Actor
from movies.models import Movie, Cast
from django.shortcuts import render

# Create your views here.

def actors_list(request):
    actors=Actor.objects.all().order_by('actor_name')
    return render(request,'actors/actors_list.html',{'actors':actors,'title': "Actors"})

def actor_details(request, slug):
    appearances = []
    try:
        actor=Actor.objects.get(slug=slug)
    except:
        return redirect('/404')
    else:
        cast = Cast.objects.filter(actor_name_id = actor.id)
        for line in cast:
            movie = Movie.objects.get(name = line.movie_name)
            # print(movie.name, movie.poster, movie.slug)
            appearance = {'movie': line.movie_name, 'role': line.role_in_movie, 'poster' : movie.poster, 'slug' : movie.slug}
            appearances.append(appearance)
        return render(request,'actors/actor_details.html', {'actor': actor, 'appearances':appearances,'title': actor.actor_name})


