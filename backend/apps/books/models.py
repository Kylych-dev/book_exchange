from django.db import models
from apps.accounts.models import CustomUser



class Book(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    public_date = models.DateField()
    page = models.IntegerField()
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    author = models.ForeignKey(to='Author', on_delete=models.CASCADE)
    genre = models.ForeignKey(to='Genre', on_delete=models.CASCADE)
    rating = models.FloatField()
    image = models.ImageField(upload_to='book_covers/')



    def __str__(self):
        return self.title


class Author(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name



class Genre(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

