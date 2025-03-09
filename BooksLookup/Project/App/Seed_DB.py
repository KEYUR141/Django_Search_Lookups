from faker import Faker
from App.models import *
import random

def seed_db(n=100):
    fake = Faker()
    authors = []

    for _ in range(10):
        authors.append(Author.objects.create(
            name = fake.name(),
            DOB = fake.date_of_birth(minimum_age=25,maximum_age=80) 
        ))

        genres = ['History','Thriller','Fictional','Non-Fictional','Science-Fictional','Adventure','Dark','Romance']

    for _ in range(n):
        Book.objects.create(
            title = fake.sentence(nb_words=4),
            author = random.choice(authors),
            genre = random.choice(genres),
            publish_date = fake.date_between(start_date='-10y', end_date='today')
        )
    print(f"{n} numbers of books are created with {len(authors)} authors")
        

    