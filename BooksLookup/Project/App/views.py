from django.shortcuts import render,HttpResponse
from App.models import *
from django.db.models import Q
from datetime import datetime
# Create your views here.

def hello(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def Search(request):
    book = Book.objects.all()

    search = request.GET.get('search')
        # Try parsing the search term as a date
    search_date = None
    
    if search:
        try:
            # Modify format according to the expected input (e.g., "March 15, 1983")
            search_date = datetime.strptime(search, '%b. %d, %Y').date()
        except ValueError:
            pass  # If parsing fails, search_date remains None
    
        #book = book.filter(genre__icontains = search)
        #book = book.filter(author__name__icontains = search)
        book = book.filter(
            Q(title__icontains = search) |
            Q(genre__icontains = search) |
            (Q(publish_date = search_date) if search_date else Q())|
            (Q(author__DOB = search_date) if search_date else Q())|
            Q(author__name__icontains = search)
        )
        
    context ={
        'book':book,
        'search':search
    }
    return render(request,'SearchBooks.html',context)