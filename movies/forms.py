from django import forms
from . import models
from django.forms import ModelForm, TextInput, EmailInput, DateInput, URLInput,FileInput, Textarea, SelectDateWidget


class AddMovie(forms.ModelForm):
    class Meta:
        model = models.Movie
        fields = ['name', 'poster', 'overview', 'director', 'release', 'runtime', 'genre']
        widgets = {
                'name':TextInput(attrs={
                'style': 'max-width:300px;',
                'style': 'display: block;',
                'placeholder':'Movie name'
            }),

            'poster': FileInput(attrs={
                'style': 'display: block;',
            }),
            'overview': Textarea(attrs={
                'rows':10,
                'cols':100,
                'style': 'display: block;',
                'placeholder': 'Overview'
            }),
            'director': TextInput(attrs={
                'style': 'max-width:300px;',
                'style': 'display: block;',
                'placeholder': 'Director'
            }),
            'release': SelectDateWidget(attrs={
                'style': 'max-width:300px;',
                'style': 'display: block;',
            }),
            'runtime': DateInput(attrs={
                'style': 'max-width:300px;',
                'style': 'display: block;',
                'placeholder': 'Runtime'
            }),
            'genre': DateInput(attrs={
                'style': 'max-width:300px;',
                'style': 'display: block;',
                'placeholder': 'Genre'
            })
        }

class AddReview(forms.ModelForm):
    class Meta:
        model = models.Review
        fields = ['review_title', 'review_rating', 'review_text']

class RateReviewLike(forms.Form):
    class Meta:
        fields=['review_likes', 'review_id']

class RateReviewDislike(forms.Form):
    class Meta:
        fields=['review_dislikes', 'review_id']

YEAR_RANGE=[('none', 'Select all')]+[(i,i) for i in range(2023,1980,-1)]
GENRES_LIST = [('none', 'Select all'),('Animation', 'Animation'), ('Action', 'Action'), ('Adventure', 'Adventure'), ('Comedy', 'Comedy'), ('Family', 'Family'), ('Fantasy', 'Fantasy'), ('Science Fiction', 'Science Fiction'), ('Horror', 'Horror'), ('War', 'War'), ('History', 'History'), ('Drama', 'Drama'), ('Thriller', 'Thriller'), ('Crime', 'Crime'), ('Mystery', 'Mystery'), ('Music', 'Music')]


class FilterForm(forms.Form):
    year = forms.CharField(label='Release year', widget=forms.Select(choices=YEAR_RANGE))
    genre = forms.CharField(label='Genre', widget=forms.Select(choices=GENRES_LIST))

