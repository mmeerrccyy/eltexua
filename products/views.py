from django.shortcuts import render
from django.views.generic import DetailView

from .models import *

# from django.http import HttpResponse
# from .models import Notebook
# Create your views here.

# def index(request):
#     latest_added = Notebook.objects.all()
#     return render(request, 'products/index.html', {'notebooks': latest_added})

def index(request):
    return render(request, 'products/wrapper.html')


class ProductDetailView(DetailView):

    CT_MODEL_MODEL_CLASS = {
        'notebook': Notebook,
        'pc': PersonalComputer,
        'tablet': Tablet,
        'smartphone': Smartphone,
        'tvset': TVset,
        'audio': Audio,
    }

    def dispatch(self, request, *args, **kwargs):
        self.model = self.CT_MODEL_MODEL_CLASS[kwargs['ct_model']]
        self.queryset = self.model._base_manager.all()
        return super().dispatch(request, *args, **kwargs)

    context_object_name = 'product'
    template_name = 'products/product_detail.html'
    slug_url_kwarg = 'slug'
