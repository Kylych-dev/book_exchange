from django.db import models
from apps.accounts.models import CustomUser


class Book(models.Model):
    title = models.CharField(max_length=100, verbose_name='Title')
    description = models.CharField(max_length=200, verbose_name='Description')
    public_date = models.DateField(verbose_name='Public Date')
    page = models.IntegerField(verbose_name='Page')
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='books')
    author = models.ForeignKey(to='Author', on_delete=models.CASCADE, related_name='books')
    genre = models.ForeignKey(to='Genre', on_delete=models.CASCADE, related_name='books')
    rating = models.FloatField(verbose_name='Rating')
    image = models.ImageField(upload_to='book_covers/', verbose_name='Image')
    isbn = models.CharField(max_length=13, unique=True, verbose_name='ISBN')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Book'
        verbose_name_plural = 'Books'
        ordering = ['title']


class Author(models.Model):
    name = models.CharField(max_length=100, verbose_name='Name')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Author'
        verbose_name_plural = 'Authors'
        ordering = ['name']


class Genre(models.Model):
    name = models.CharField(max_length=100, verbose_name='Name')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Genre'
        verbose_name_plural = 'Genres'
        ordering = ['name']

