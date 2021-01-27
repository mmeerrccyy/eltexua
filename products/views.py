from django.shortcuts import render
from django.views.generic import DetailView, View

from .models import *
from .mixins import CategoryDetailMixin

# from django.http import HttpResponse
# from .models import Notebook
# Create your views here.

# def index(request):
#     latest_added = Notebook.objects.all()
#     return render(request, 'products/index.html', {'notebooks': latest_added})


# def index(request):
#
#     categories = Category.objects.get_categories_for_left_sidebar()
#     return render(request, 'products/index.html', {'categories': categories})
class BaseView(View):

    def get(self, request, *args, **kwargs):
        categories = Category.objects.get_categories_for_left_sidebar()
        products = LatestProducts.objects.get_products_for_main_page('notebook')
        context = {
            'categories': categories,
            'products': products
        }
        return render(request, 'products/index.html', context)


class ProductDetailView(CategoryDetailMixin, DetailView):

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


class CategoryDetailView(CategoryDetailMixin, DetailView):

    model = Category
    queryset = Category.objects.all()
    context_name = 'category'
    template_name = 'products/category_detail.html'
    slug_url_kwarg = 'slug'


class CartView(View):

    def get(self, request, *args, **kwargs):
        categories = Category.objects.get_categories_for_left_sidebar()
        customer = Customer.objects.get(user = request.user)
        cart = Cart.objects.get(owner = customer)
        context = {
            'cart': cart,
            'categories': categories,
        }
        return render(request, 'products/cart.html', context)