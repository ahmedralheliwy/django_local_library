from django.shortcuts import render 
from .models import Book,Author,BookInstance,Genre,Language
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin

# Create your views here.

def index(request):
    # Generate counts of some of the main objects
    num_books=Book.objects.all().count()
    num_instance=BookInstance.objects.all().count()

    # Available books (status='a')
    num_instances_available=BookInstance.objects.filter(status__exact='a').count

    # The 'all()' is implied by default.

    num_authors=Author.objects.count()
    
    # Number of visits to this view
    num_visits=request.session.get('num_visits',0)
    request.session['num_visits']=num_visits+1

    context={
            'num_books':num_books,
            'num_instance':num_instance,
            'num_instances_available':num_instances_available,
            'num_authors':num_authors,
            'num_visits':num_visits,
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


class BookDetailView(LoginRequiredMixin,generic.DetailView):
    login_url='/accounts/login'
    redirect_field_name='redirect_to'
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

class LoanedBooksByUserListView(LoginRequiredMixin,generic.ListView):
    model=BookInstance
    template_name='catalog/bookinstance_list_borrowed_user.html'
    paginate_by=10

    def get_queryset(self):
        return (BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back'))

class BorrowedBooksListView(LoginRequiredMixin,PermissionRequiredMixin,generic.ListView):
    model=BookInstance
    template_name='catalog/bookinstance_list_borrowed_books.html'
    paginate_by=10
    permission_required=('catalog.can_mark_returned',)

    def get_queryset(self):
        return (BookInstance.objects.filter(status__exact='o').order_by('due_back'))

