from django.db import models

# Create your models here.

class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=50)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Book"
        verbose_name_plural = "Books"