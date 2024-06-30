from django.shortcuts import render
from .models import Book,Author,BookInstance,Genre,Language

# Create your views here.

def index(request):
    # Generate counts of some of the main objects
    num_books=Book.objects.all().count()
    num_instance=BookInstance.objects.all().count()

    # Available books (status='a')
    num_instances_available=BookInstance.objects.filter(status_exact='a').count

    # The 'all()' is implied by default.

    num_authors=Author.objects.count()

    context={
            'num_books':num_books,
            'num_instance':num_instance,
            'num_instances_available':num_instances_available,
            'num_authors':num_authors,
            }

    # Render the html template index.html with the data in the context variable

    return render(request,'index.html',context=context)

#see you later.