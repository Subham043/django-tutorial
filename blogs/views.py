from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from .models import Article 
from .forms import NameForm, ArticleForm
from django.views.generic import TemplateView, DetailView, ListView
from django.utils import timezone
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.urls import reverse_lazy
import csv

# Create your views here.
    
class MyView(View):
    def get(self, request):
        # <view logic>
        return render(request, 'blogs/test.html')
        return HttpResponse('result')
    
class GreetingView(View):
    greeting = "Good Day"

    def get(self, request):
        return HttpResponse(self.greeting)
    
class MorningGreetingView(GreetingView):
    greeting = "Morning to ya"

class FormView(View):
    def get(self, request):
        # <view logic>
        form = ArticleForm()
        return render(request, 'blogs/form.html', {'form': form})
    
class TempView(TemplateView):
    template_name = "blogs/form.html" #template name

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ArticleForm()
        return context
    
class ArticleListView(ListView):
    paginate_by = 1
    model = Article
    queryset = Article.objects.order_by('-publish_on')
    context_object_name = 'my_favorite_articles'

class ArticleDetailView(DetailView):

    context_object_name = 'article'
    queryset = Article.objects.all()

    def get_object(self):
        obj = super().get_object()
        # Record the last accessed date
        obj.updated_at = timezone.now()
        obj.save()
        return obj
    
class ArticleFormView(FormView):
    template_name = 'form.html'
    form_class = NameForm
    success_url = '/thanks/'

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        form.send_email()
        return super().form_valid(form)
    
class ArticleCreateView(CreateView):
    model = Article
    fields = ['title']

class ArticleUpdateView(UpdateView):
    model = Article
    fields = ['title']
    template_name_suffix = '_update_form'

class ArticleDeleteView(DeleteView):
    model = Article
    success_url = reverse_lazy('blogs:article_list_view')


def csv_view(request):
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(
        content_type='text/csv',
        headers={'Content-Disposition': 'attachment; filename="somefilename.csv"'},
    )

    writer = csv.writer(response)
    writer.writerow(['First row', 'Foo', 'Bar', 'Baz'])
    writer.writerow(['Second row', 'A', 'B', 'C', '"Testing"', "Here's a quote"])

    return response