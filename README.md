# Django_Search_Lookups
It is my project for practice type, were I learned about how the search lookups are performed in python framework called Django, which is used in backend web development.

<div class="container mt-5">
    <h1 class="mb-4">Django Search Lookups</h1>
    <p>This project demonstrates how to implement search lookups in a Django application. Follow the step-by-step guide below to understand the process:</p>
    
    <h2>1. Created Models</h2>
    <pre><code>
from django.db import models

class Author(models.Model):
    name = models.CharField(max_length=100)
    DOB = models.DateField(blank=True, null=True)

    def __str__(self):
        return self name

class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    genre = models.CharField(max_length=100)
    publish_date = models.DateField()

    def __str__(self):
        return self title
    </code></pre>
    <img src="path/to/your/screenshot.png" alt="Models Screenshot" width="600" class="my-3">
    
    <h2>2. Used Faker for Inserting Fake and Unique Data</h2>
    <pre><code>
from faker import Faker
from App.models import *
import random

def seed_db(n=100):
    fake = Faker()
    authors = []

    for _ in range(10):
        authors.append(Author.objects.create(
            name=fake.name(),
            DOB=fake.date_of_birth(minimum_age=25, maximum_age=80)
        ))

    genres = ['History', 'Thriller', 'Fictional', 'Non-Fictional', 'Science-Fictional', 'Adventure', 'Dark', 'Romance']

    for _ in range(n):
        Book.objects.create(
            title=fake.sentence(nb_words=4),
            author=random.choice(authors),
            genre=random.choice(genres),
            publish_date=fake.date_between(start_date='-10y', end_date='today')
        )
    print(f"{n} books created with {len(authors)} authors")
    </code></pre>
    
    <h2>3. Added the Logic in <code>views.py</code></h2>
    <pre><code>
from django.shortcuts import render, HttpResponse
from App.models import *
from django.db.models import Q
from datetime import datetime

def hello(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def Search(request):
    book = Book.objects.all()
    search = request.GET.get('search')
    search_date = None

    if search:
        try:
            search_date = datetime.strptime(search, '%b. %d, %Y').date()
        except ValueError:
            pass  # If parsing fails, search_date remains None

        book = book.filter(
            Q(title__icontains=search) |
            Q(genre__icontains=search) |
            (Q(publish_date=search_date) if search_date else Q()) |
            (Q(author__DOB=search_date) if search_date else Q()) |
            Q(author__name__icontains=search)
        )

    context = {
        'book': book,
        'search': search
    }
    return render(request, 'SearchBooks.html', context)
    </code></pre>
    
    <h2>4. Create HTML Page in Template</h2>
    <pre><code>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-QWTKZyjpPEjISv5WaRU9OFeRpok6YctnYmDr5pNlyT2bRjXh0JMhjY6hW+ALEwIH" crossorigin="anonymous">
</head>
<body>
  <form method="get">
    {% csrf_token %}
    <div class="container-fluid m-5">
      <div class="search_box mt-2">
        <input type="search" placeholder="Search books or Authors" value="{{search}}" class="form-control" name="search">
        <br>
        <button class="btn btn-success">Search</button>
      </div>
    </div>
  </form>
    <div class="table table-responsive">
    <table class="table table-striped table-dark">
        <thead>
          <tr>
            <th scope="col">#</th>
            <th scope="col">Book Title</th>
            <th scope="col">Book Authors</th>
            <th scope="col">Authors Birth Date</th>
            <th scope="col">Genre</th>
            <th scope="col">Date of Book Publication</th>
          </tr>
        </thead>
        <tbody>
          {% for b in book %}
        <tr>
        <th scope="row">{{forloop.counter}}</th>
        <td>{{b.title}}</td>
        <td>{{b.author}}</td>
        <td>{{b.author.DOB}}</td>
        <td>{{b.genre}}</td>
        <td>{{b.publish_date}}</td>
        </tr>
        {% endfor %}
        </tbody>
    </table>
    </div>
</body>
</html>
    </code></pre>
    
    <h2>5. Conclusion</h2>
    <p>This project was created to understand how lookup searches work in Django. By following these steps, you can implement similar search functionality in your Django applications.</p>
</div>