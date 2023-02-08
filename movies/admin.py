from django.contrib import admin
from .models import *

admin.site.register(Movie)
# admin.site.register(Actor)
admin.site.register(Cast)
admin.site.register(Review)

