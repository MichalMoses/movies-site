from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import *
from actors.models import Actor
from . import forms
from django.utils.text import slugify



# the following function builds the main page of the site containing all the movies posters previews
def movie_list(request): #todo take care of the filter clear button
    filter = {'none': 0, 'filtered': 0, 'empty': 0} #filter dict initialized
    movies_unfiltered = Movie.objects.all().order_by('-rating_avg') #get all the movies from DB sorted by average rating
    if request.method=="POST": #filter button was pressed
        form = forms.FilterForm(request.POST)
        if form.is_valid():
            fdata = form.cleaned_data #get the filter data
            year = fdata.get('year')
            genre = fdata.get('genre')
        # check the data in the filters and apply filters accordingly
        if genre == 'none' and year=='none': #filter button was pressed but values are both 'select all', no filters to apply
            movies = movies_unfiltered
            filter['none'] = 1
        elif year == 'none': #only genre filter is applied
            movies = movies_unfiltered.filter(genre__contains=genre)
            filter['filtered'] = 1
        elif genre == 'none': #only year filter is applied
            movies = movies_unfiltered.filter(release__contains=year)
            filter['filtered'] = 1
        else:   #both year and genre filters applied
            movies=movies_unfiltered.filter(genre__contains=genre, release__contains=year)
            filter['filtered'] = 1

    else: #if filter button not pressed
        movies = movies_unfiltered
        form = forms.FilterForm()
        filter['none']=1
    movie_count = movies.count()
    if not movie_count: #if there are no movies to display update the filters dictionary
        filter.update({'none': 0, 'filtered': 0, 'empty': 1})
    return render(request, 'movies/movies_list.html', {'movies':movies, 'movie_count': movie_count , 'form':form, 'filter' : filter, 'title': "Movies" })

#following funciton builds the page of a specific movie
def movie_details(request, slug):
    try:
        movie = Movie.objects.get(slug=slug) #find the movie with the required slug
    except:
        return redirect('/404')
    else:
        if request.method=="POST": #two forms in the page are for rating the review. one from for "like" another form for "dislike"
            rated_review_id = request.POST.get('review_id')  # get the id of the review that is being rated from the form
            review=Review.objects.get(id=rated_review_id) #get the instance of the review being rated from Review table in DB
            if request.POST.get('review_like'): #if the form that was sent is the "like" form, increment like
                review.review_likes += 1
            elif request.POST.get('review_dislike'): #if the form that was sent is the "dislike" from, increment dislike
                review.review_dislikes +=1
            review.save() #save and redirect to the same page, to the same location in page (the review that was rated)
            review_url=f'/movies/{movie.slug}#{rated_review_id}'
            return redirect(review_url)

        #building the page display (no form button pressed)
        cast = Cast.objects.all().filter(movie_name_id = movie.id) #get the cast of the movie from Cast table in DB (multiple rows)
        cast_list = [] #cast list will contain the actors full details in dictionaries
        for role in cast: #get the full data for each actor in cast and update cast_list
            actor = Actor.objects.get(actor_name = role.actor_name)
            actor_details = {'name': role.actor_name, 'role': role.role_in_movie, 'image':actor.actor_image.url, 'slug': actor.slug}
            cast_list.append(actor_details)
        #get all the reviews written on the movie
        reviews = Review.objects.all().filter(review_movie_name = movie.id).order_by('-review_likes')
        reviews_list=[] #review list will contain dictionaires with the reviews details relevant
        for review in reviews: #for each review build the forms for like and dislike
            form_like=forms.RateReviewLike()
            form_dislike=forms.RateReviewDislike()
            reviews_list.append({'review':review, 'range_ostar':range(review.review_rating), 'range_dstar': range(5-review.review_rating), 'form_like':form_like, 'form_dislike':form_dislike})
        return render(request, 'movies/movie_details.html', {'movie':movie, 'cast_list':cast_list, 'reviews_list':reviews_list, 'title': movie.name})


#following function builds the page for adding a new movie. function is restricted to superusers only
@login_required(login_url='/accounts/login')
@user_passes_test(lambda u: u.is_superuser)
def movie_create(request):
    if request.method=='POST': #if form submitted
        form = forms.AddMovie(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)  #get the data from the form
            instance.author = request.user  #update user
            instance.rating_avg = 0     #when movie is just created there are no ratings yet
            instance.rating_num = 0
            instance.slug=slugify(instance.name)
            instance.save()
            return redirect('movies:list')
    else:
        form=forms.AddMovie()
    return render(request, 'movies/add_new_movie.html', {'form':form,'title': "Add Movie"})

#function for adding review to a movie. accessible only for logged in users
@login_required(login_url='/accounts/login')
def add_review(request, slug):
    movie = Movie.objects.get(slug=slug) #get the details of the movie that is being reviewd
    print(f'--DEBUG movie: {movie}')
    if request.method == 'POST':
        form = forms.AddReview(request.POST) #get the data from the review form
        if form.is_valid():
            instance = form.save(commit=False)
            instance.review_author = request.user
            instance.review_movie_name = movie
            instance.save()
            movie.rating_avg = round((movie.rating_num * movie.rating_avg + instance.review_rating)/(movie.rating_num+1),1) #update the average rating of the movie with the current review
            movie.rating_num += 1 #increment the number of ratings for the average
            movie.save()
            redirect_url=f'/movies/{movie.slug}#reviews'
            return redirect(redirect_url, slug=slug)
    else:
        form = forms.AddReview() #generate the page with a blank form
    return render(request, 'movies/add_review.html', {'form':form, 'slug':slug, 'movie':movie.name ,'title': "Add review"})