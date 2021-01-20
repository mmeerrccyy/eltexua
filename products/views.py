from django.shortcuts import render
from django.http import HttpResponse
from .models import Notebook
# Create your views here.

def index(request):
    latest_added = Notebook.objects.all()
    return render(request, 'products/index.html', {'notebooks': latest_added})