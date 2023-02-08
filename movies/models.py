from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from actors import models as actors_models

# Create your models here.
class Movie(models.Model):
    poster = models.ImageField(default='default_poster.jpg', blank=True)
    name = models.CharField(max_length=100)
    slug = models.SlugField(default=None,)
    overview = models.TextField(default=None)
    director = models.CharField(default=None, max_length=50)
    release = models.DateField(default=None,)
    runtime = models.CharField(default=None, max_length=20)
    genre = models.TextField(default=None)
    rating_avg = models.FloatField(default=None)
    rating_num = models.IntegerField(default=None)
    author = models.ForeignKey(User, default=None, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Cast(models.Model):
    actor_name = models.ForeignKey(actors_models.Actor, default=None, on_delete=models.CASCADE)
    movie_name = models.ForeignKey(Movie, default=None, on_delete=models.CASCADE)
    role_in_movie = models.CharField(max_length=30)

    def __str__(self):
        return f'{self.actor_name} as {self.role_in_movie} in the movie "{self.movie_name}"'


class Review(models.Model):
    review_movie_name = models.ForeignKey(Movie, default=None, on_delete=models.CASCADE)
    review_title = models.CharField(max_length=100)
    review_rating = models.IntegerField(default=5, validators=[MaxValueValidator(5), MinValueValidator(1)])
    review_text = models.TextField(default=None, blank=True)
    review_date = models.DateTimeField(auto_now_add=True)
    review_author = models.ForeignKey(User, default=None, on_delete=models.CASCADE)
    review_likes = models.IntegerField(default=0)
    review_dislikes = models.IntegerField(default=0)

    def __str__(self):
        return f'Title: {self.review_title} Movie: {self.review_movie_name} '