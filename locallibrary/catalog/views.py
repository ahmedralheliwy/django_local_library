from django.shortcuts import render , get_object_or_404
from .models import Book,Author,BookInstance,Genre,Language
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
from django.contrib.auth.decorators import login_required,permission_required
from django.http import HttpResponseRedirect
from django.urls import reverse
from catalog.forms import RenewBookForm 
import datetime

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



@login_required
@permission_required('catalog.can_mark_returned',raise_exception=True)
def renew_book_librarian(request,pk):
    book_instance=get_object_or_404(BookInstance,pk=pk)
    if request.method=='POST':
        form=RenewBookForm(request.POST)
        if form.is_valid():
            book_instance.due_back=form.cleaned_data['renewal_date']
            book_instance.save()
            return HttpResponseRedirect(reverse('borrowed'))

    else:
        proposed_renewal_date=datetime.date.today() + datetime.timedelta(weeks=3)
        form=RenewBookForm(initial={'renewal_date':proposed_renewal_date})
        context={'form':form,'book_instance':book_instance}

    return render(request,'catalog/book_renew_librarian.html',context)

