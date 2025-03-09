from django.db import models

# Create your models here.
class Author(models.Model):
    name  = models.CharField(max_length=100)
    DOB = models.DateField(blank=True,null=True)

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    genre = models.CharField(max_length=100)
    publish_date = models.DateField()

    def __str__(self):
        return self.title
    
