# Django_Search_Lookups
<h1>Django Search Lookups</h1>
<p>Search lookups in Django enable you to perform full-text searches on fields like `CharField` or `TextField`, allowing you to filter records based on specific text patterns. This is achieved through the `search` lookup, which relies on your database's full-text search capabilities. For instance, if you're using PostgreSQL, its robust full-text search support ensures efficient query processing. However, it's important to index the relevant fields in your database for optimal search performance. Additionally, the behavior of the search, such as whether it's case-sensitive, depends on your database and its configuration. By leveraging search lookups, Django simplifies the process of querying text data, making it a powerful tool for building applications that rely on keyword-based filtering and search functionality. If you'd like, I can guide you through setting up these features in your project!</p>

<h2>Creating Models in Django</h2>

<p>This code demonstrates how to use Django models to store information about books and their authors. The <strong>Author</strong> model represents authors with fields for their name and date of birth, while the <strong>Book</strong> model stores information about books, including their title, author, genre, and publication date. A relationship is established between books and authors using a foreign key.</p>

<div style="background-color: #f9f9f9; padding: 10px; border: 1px solid #ddd; border-radius: 5px; font-family: 'Courier New', monospace;">
<pre>
from django.db import models

# Create your models here.
class Author(models.Model):
    name  = models.CharField(max_length=100)
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
</pre>
</div>

<h3>Explanation:</h3>
<ul>
    <li>The <strong>Author</strong> model defines fields for an author's name (<code>CharField</code>) and date of birth (<code>DateField</code>). The <code>__str__</code> method returns the author's name.</li>
    <li>The <strong>Book</strong> model defines fields for a book's title, genre, and publication date, and it establishes a relationship with the <strong>Author</strong> model via a foreign key. The <code>on_delete=models.CASCADE</code> ensures that deleting an author also deletes their associated books.</li>
    <li>The <code>__str__</code> method of the <strong>Book</strong> model returns the book's title.</li>
</ul>

