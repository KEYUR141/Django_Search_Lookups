# Django Search Lookups

## Introduction
Django provides powerful search capabilities through its ORM (Object-Relational Mapping). In this project, we implement search lookups for a book database using `Q` objects. This allows users to search books by title, genre, author's name, and even dates like the book's publication date or the author's date of birth.

---

## 1. Creating Models in the App
We begin by defining models for `Author` and `Book` in our Django application:

```python
from django.db import models

# Create your models here.
class Author(models.Model):
    name = models.CharField(max_length=100)
    DOB = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    genre = models.CharField(max_length=100)
    publish_date = models.DateField()

    def __str__(self):
        return self.title
```

---

## 2. Seeding the Database with Faker
To generate realistic fake data, we use the `Faker` library:

```python
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
```

---

## 3. Implementing the View Logic
The search functionality is implemented using Django's `Q` objects:

```python
from django.shortcuts import render, HttpResponse
from App.models import *
from django.db.models import Q
from datetime import datetime

# Create your views here.
def hello(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def Search(request):
    books = Book.objects.all()
    search = request.GET.get('search')
    search_date = None

    if search:
        try:
            search_date = datetime.strptime(search, '%b. %d, %Y').date()
        except ValueError:
            pass  # If parsing fails, search_date remains None

        books = books.filter(
            Q(title__icontains=search) |
            Q(genre__icontains=search) |
            (Q(publish_date=search_date) if search_date else Q()) |
            (Q(author__DOB=search_date) if search_date else Q()) |
            Q(author__name__icontains=search)
        )
    
    context = {
        'book': books,
        'search': search
    }
    return render(request, 'SearchBooks.html', context)
```

---

## 4. Search Page Template (HTML)
The `SearchBooks.html` template provides a simple UI for searching books:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Search Books</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
  <form method="get">
    {% csrf_token %}
    <div class="container-fluid m-5">
      <div class="search_box mt-2">
        <input type="search" placeholder="Search books or Authors" value="{{ search }}" class="form-control" name="search">
        <br>
        <button class="btn btn-success">Search</button>
      </div>
    </div>
  </form>

  <div class="table table-responsive">
    <table class="table table-striped table-dark">
        <thead>
          <tr>
            <th>#</th>
            <th>Book Title</th>
            <th>Book Author</th>
            <th>Author's Birth Date</th>
            <th>Genre</th>
            <th>Publication Date</th>
          </tr>
        </thead>
        <tbody>
          {% for b in book %}
        <tr>
        <th>{{ forloop.counter }}</th>
        <td>{{ b.title }}</td>
        <td>{{ b.author }}</td>
        <td>{{ b.author.DOB }}</td>
        <td>{{ b.genre }}</td>
        <td>{{ b.publish_date }}</td>
        </tr>
        {% endfor %}
        </tbody>
    </table>
  </div>
</body>
</html>
```

---

## 5. Conclusion
In this project, we implemented Django search lookups using `Q` objects to filter books based on title, genre, author's name, and dates. We also used the `Faker` library to populate our database with realistic data. This approach provides a flexible way to search and filter data in a Django application.

