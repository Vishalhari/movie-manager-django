from django.db import models

# Create your models here.
class Genre(models.Model):
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=200)

    def __str__(self):
        return '{}'.format(self.title)

class Movies(models.Model):
    title = models.CharField(max_length=200)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    description = models.CharField(max_length=200)
    releaseDate = models.DateField(max_length=200)
    actors = models.CharField(max_length=200)
    banner = models.ImageField(upload_to="movies")
    imdbrating = models.CharField(max_length=200,default=0.0)
    trailerLink = models.CharField(max_length=500)

    def __str__(self):
        return '{}'.format(self.title)



