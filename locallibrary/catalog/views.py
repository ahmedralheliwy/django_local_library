from django.shortcuts import render 
from .models import Book,Author,BookInstance,Genre,Language
from django.views import generic

# Create your views here.

def index(request):
    # Generate counts of some of the main objects
    num_books=Book.objects.all().count()
    num_instance=BookInstance.objects.all().count()

    # Available books (status='a')
    num_instances_available=BookInstance.objects.filter(status__exact='a').count

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

class BookListView(generic.ListView):
    model = Book
    paginate_by=3

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super(BookListView, self).get_context_data(**kwargs)
        # Create any data and add it to the context
        context['some_data'] = 'This is just some data'
        return context


class BookDetailView(generic.DetailView):
    model=Book
    

class AuthorListView(generic.ListView):
    model=Author
    def get_context_data(self,**kwargs):
        context=super(AuthorListView,self).get_context_data(**kwargs)
        context['some_data_of_author']='This is just some data about author'
        return context

class AuthorDetailView(generic.DetailView):
    model=Author
    template_name='catalog/author_detail.html'
