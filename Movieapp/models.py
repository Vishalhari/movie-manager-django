from django.db import models
from django.contrib.auth.models import User
import datetime

# Create your models here.
class Genre(models.Model):
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=200)

    def __str__(self):
        return '{}'.format(self.title)

class Movies(models.Model):
    title = models.CharField(max_length=200)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    users = models.ForeignKey(User,on_delete=models.CASCADE,default=1)
    description = models.CharField(max_length=500)
    releaseDate = models.DateField(max_length=200)
    actors = models.CharField(max_length=200)
    banner = models.ImageField(upload_to="movies")
    imdbrating = models.CharField(max_length=200,default=0.0)
    trailerLink = models.CharField(max_length=500)
    approval_status = models.IntegerField(default=1)

    def __str__(self):
        return '{}'.format(self.title)

class Reviews(models.Model):
    rating  = models.IntegerField()
    review = models.CharField(max_length=500)
    MovieId = models.ForeignKey(Movies,on_delete=models.CASCADE,default=1)
    UserId = models.ForeignKey(User,on_delete=models.CASCADE,default=1)
    created = models.DateTimeField(default=datetime.datetime.now)
    active = models.IntegerField(default=0)

    def __str__(self):
        return '{}'.format(self.rating)






