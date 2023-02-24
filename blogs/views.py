from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views import View
from .models import Article 
from .forms import NameForm, ArticleForm
from django.views.generic import TemplateView, DetailView, ListView
from django.utils import timezone
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.http import Http404
from django.contrib.auth.models import User
import csv

#rest framework
from rest_framework.parsers import JSONParser
from blogs.serializers import ArticleSerializer, ArticleModelSerializer, UserSerializer
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import mixins
from rest_framework import generics


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

# """
# rest framework
# """

#function views
@api_view(['GET', 'POST'])
def article_list(request):
    """
    List all code articles, or create a new article.
    """
    if request.method == 'GET':
        articles = Article.objects.all()
        serializer = ArticleModelSerializer(articles, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ArticleModelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['GET', 'PUT', 'DELETE'])
def article_detail(request, pk):
    """
    Retrieve, update or delete a code article.
    """
    try:
        article = Article.objects.get(pk=pk)
    except Article.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ArticleSerializer(article)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = ArticleSerializer(article, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

#class based views
class ArticleList(APIView):
    """
    List all articles, or create a new article.
    """
    def get(self, request, format=None):
        articles = Article.objects.all()
        serializer = ArticleModelSerializer(articles, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = ArticleModelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ArticleDetail(APIView):
    """
    Retrieve, update or delete a article instance.
    """
    def get_object(self, pk):
        try:
            return Article.objects.get(pk=pk)
        except Article.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        article = self.get_object(pk)
        serializer = ArticleModelSerializer(article)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        article = self.get_object(pk)
        serializer = ArticleModelSerializer(article, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        article = self.get_object(pk)
        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

#class based mixin views
class ArticleMixinList(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  generics.GenericAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleModelSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
    
class ArticleMixinDetail(mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    generics.GenericAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleModelSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


#class based generic views
class ArticleGenericList(generics.ListCreateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleModelSerializer


class ArticleGenericDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleModelSerializer

class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
