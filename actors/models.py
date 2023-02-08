from django.db import models

class Actor(models.Model):
    actor_name = models.CharField(max_length=30)
    actor_image = models.ImageField(default='default_actor.jpg', blank=True)
    actor_gender = models.CharField(max_length=30)
    actor_birthday = models.DateField(default=None)
    actor_place_of_birth = models.CharField(max_length=100)
    slug = models.SlugField(default=None)

    def __str__(self):
        return self.actor_name