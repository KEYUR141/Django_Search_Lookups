# Django_Search_Lookups
<h1>Django Search Lookups</h1>
<p>Search lookups in Django enable you to perform full-text searches on fields like `CharField` or `TextField`, allowing you to filter records based on specific text patterns. This is achieved through the `search` lookup, which relies on your database's full-text search capabilities. For instance, if you're using PostgreSQL, its robust full-text search support ensures efficient query processing. However, it's important to index the relevant fields in your database for optimal search performance. Additionally, the behavior of the search, such as whether it's case-sensitive, depends on your database and its configuration. By leveraging search lookups, Django simplifies the process of querying text data, making it a powerful tool for building applications that rely on keyword-based filtering and search functionality. If you'd like, I can guide you through setting up these features in your project!</p>

<h1>Book and Author Search Application in Django</h1>

<div class="section">
    <h2>Overview</h2>
    <p>This project demonstrates the implementation of a search functionality in a Django application using search lookups. It allows users to search for books and authors based on various attributes, such as book title, genre, publication date, or the author's birthdate.</p>
</div>

<div class="section">
    <h2>I. Creating Models in Django</h2>
    <p>The application defines models for <code>Author</code> and <code>Book</code> to manage and store data in the database.</p>
    <pre><code>
from django.db import models

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
    </code></pre>
    <div class="screenshot-placeholder">📌 Add screenshots of your model structure and data in the admin panel here.</div>
</div>

<div class="section">
    <h2>II. Generating Fake Data Using Faker Library</h2>
    <p>To populate the database with test data, we utilize the <code>Faker</code> library. The script <code>seed_db.py</code> automates the creation of sample authors and books.</p>
    <h3>What is Faker?</h3>
    <p>The <code>Faker</code> library generates random, realistic test data such as names, dates, addresses, and more. It simplifies testing by populating the database quickly.</p>
    <pre><code>
from App.models import *
import random
from faker import Faker

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

    print(f"{n} numbers of books are created with {len(authors)} authors")
    </code></pre>
</div>

<div class="section">
    <h2>III. Search Logic in Views</h2>
    <p>The search feature uses Django's QuerySets and <code>Q</code> objects to allow users to filter books and authors based on the title, genre, publication date, or the author's name or birthdate.</p>
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
            pass

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
</div>

<div class="section">
    <h2>IV. Creating the Search HTML Page</h2>
    <p>The HTML page provides an interface for users to enter search queries and displays the results dynamically. It uses Bootstrap for styling and includes a CSRF token for secure form submissions.</p>
    <pre><code>
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
<div class="table-responsive">
    <table class="table table-striped table-dark">
        <thead>
            <tr>
                <th>#</th>
                <th>Book Title</th>
                <th>Book Authors</th>
                <th>Author's Birth Date</th>
                <th>Genre</th>
                <th>Publication Date</th>
            </tr>
        </thead>
        <tbody>
            {% for b in book %}
            <tr>
                <td>{{ forloop.counter }}</td>
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
    </code></pre>
    <div class="screenshot-placeholder">📌 Add a screenshot of the rendered search page showing the results here.</div>
</div>

<div class="section">
    <h2>V. Outputs</h2>
    <p>Here are examples of the search functionality in action:</p>
    <div class="screenshot-placeholder">📌 Add screenshots of search results filtered by title, genre, or author here.</div>
</div>

<div class="section">
    <h2>VI. Conclusion</h2>
    <p>This project demonstrates the creation of a Django application with advanced search functionality. By using Django models, views, templates, and external libraries like Faker, it showcases how to build and manage robust web applications. The search implementation using Django QuerySets and <code>Q</code> objects is particularly powerful and efficient, making this project a great example of Django's capabilities.</p>
</div>


