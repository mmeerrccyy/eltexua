from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.db import transaction
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render
from django.views.generic import DetailView, View

from .forms import OrderForm, LoginForm, RegistrationForm
from .mixins import CategoryDetailMixin, CartMixin
from .models import *
from .utils import recalc_cart

class BaseView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        categories = Category.objects.get_categories_for_left_sidebar()
        notebooks = LatestProducts.objects.get_products_for_main_page('notebook')
        smartphones = LatestProducts.objects.get_products_for_main_page('smartphone')
        tvsets = LatestProducts.objects.get_products_for_main_page('tvset')
        tablets = LatestProducts.objects.get_products_for_main_page('tablet')
        audios = LatestProducts.objects.get_products_for_main_page('audio')
        pcs = LatestProducts.objects.get_products_for_main_page('personalcomputer')
        context = {
            'categories': categories,
            'notebooks': notebooks,
            'smartphones': smartphones,
            'tvsets': tvsets,
            'tablets': tablets,
            'audios': audios,
            'pcs': pcs,
            'cart': self.cart
        }
        return render(request, 'products/index.html', context)


class ProductDetailView(CartMixin, CategoryDetailMixin, DetailView):
    CT_MODEL_MODEL_CLASS = {
        'notebook': Notebook,
        'personalcomputer': PersonalComputer,
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ct_model'] = self.model._meta.model_name
        context['cart'] = self.cart
        return context


class CategoryDetailView(CartMixin, CategoryDetailMixin, DetailView):
    model = Category
    queryset = Category.objects.all()
    context_name = 'category'
    template_name = 'products/category_detail.html'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cart'] = self.cart
        return context


class AddToCartView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            ct_model, product_slug = kwargs.get('ct_model'), kwargs.get('slug')
            content_type = ContentType.objects.get(model=ct_model)
            product = content_type.model_class().objects.get(slug=product_slug)
            cart_product, created = CartProduct.objects.get_or_create(
                user=self.cart.owner,
                cart=self.cart,
                content_type=content_type,
                object_id=product.id,
            )
            if created:
                self.cart.products.add(cart_product)
            recalc_cart(self.cart)
            messages.add_message(request, messages.INFO, 'Товар успішно додано!')
            return HttpResponseRedirect('/cart/')
        else:
            raise Http404('Сторінки не існує')


class DeleteFromCartView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            ct_model, product_slug = kwargs.get('ct_model'), kwargs.get('slug')
            content_type = ContentType.objects.get(model=ct_model)
            product = content_type.model_class().objects.get(slug=product_slug)
            cart_product = CartProduct.objects.get(
                user=self.cart.owner,
                cart=self.cart,
                content_type=content_type,
                object_id=product.id,
            )
            self.cart.products.remove(cart_product)
            cart_product.delete()
            recalc_cart(self.cart)
            messages.add_message(request, messages.INFO, 'Товар успішно видалено!')
            return HttpResponseRedirect('/cart/')
        else:
            raise Http404('Сторінки не існує')


class ChangeQTYView(CartMixin, View):

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            ct_model, product_slug = kwargs.get('ct_model'), kwargs.get('slug')
            content_type = ContentType.objects.get(model=ct_model)
            product = content_type.model_class().objects.get(slug=product_slug)
            cart_product = CartProduct.objects.get(
                user=self.cart.owner,
                cart=self.cart,
                content_type=content_type,
                object_id=product.id,
            )
            qty = int(request.POST.get('qty'))
            cart_product.qty = qty
            cart_product.save()
            recalc_cart(self.cart)
            messages.add_message(request, messages.INFO, 'Кількість товару успішно зміненно!')
            return HttpResponseRedirect('/cart/')
        else:
            raise Http404('Сторінки не існує')


class CartView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            categories = Category.objects.get_categories_for_left_sidebar()
            context = {
                'cart': self.cart,
                'categories': categories,
            }
            return render(request, 'products/cart.html', context)
        else:
            raise Http404('Сторінки не існує')


class CheckoutView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            categories = Category.objects.get_categories_for_left_sidebar()
            form = OrderForm(request.POST or None)
            context = {
                'cart': self.cart,
                'categories': categories,
                'form': form,
            }
            return render(request, 'products/checkout.html', context)
        else:
            raise Http404('Сторінки не існує')


class MakeOrderView(CartMixin, View):

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            form = OrderForm(request.POST or None)
            customer = Customer.objects.get(user=request.user)
            if form.is_valid():
                new_order = form.save(commit=False)
                new_order.customer = customer
                new_order.first_name = form.cleaned_data['first_name']
                new_order.last_name = form.cleaned_data['last_name']
                new_order.phone = form.cleaned_data['phone']
                new_order.address = form.cleaned_data['address']
                new_order.buying_type = form.cleaned_data['buying_type']
                new_order.order_date = form.cleaned_data['order_date']
                new_order.comment = form.cleaned_data['comment']
                new_order.save()
                self.cart.in_order = True
                self.cart.save()
                new_order.cart = self.cart
                new_order.save()
                customer.orders.add(new_order)
                messages.add_message(request, messages.INFO, 'Замовлення успішно відправленно на обробку!')
                return HttpResponseRedirect('/')
            messages.add_message(request, messages.INFO, 'Ой, щось пішло не так')
            return HttpResponseRedirect('/checkout/')
        else:
            raise Http404('Сторінки не існує')


class LoginView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            form = LoginForm(request.POST or None)
            categories = Category.objects.get_categories_for_left_sidebar()
            context = {
                'form': form,
                'categories': categories,
                'cart': self.cart,
            }
            return render(request, 'products/login.html', context)
        else:
            raise Http404('Сторінки не існує')

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST or None)
        categories = Category.objects.get_categories_for_left_sidebar()
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return HttpResponseRedirect('/')
            context = {
                'form': form,
                'cart': self.cart,
                'categories': categories
            }
        return render(request, 'products/login.html', {'form': form, 'cart': self.cart})


class RegistrationView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            form = RegistrationForm(request.POST or None)
            categories = Category.objects.get_categories_for_left_sidebar()
            context = {
                'form': form,
                'categories': categories,
                'cart': self.cart
            }
            return render(request, 'products/registration.html', context)
        else:
            raise Http404('Сторінки не існує')

    def post(self, request, *args, **kwargs):
        form = RegistrationForm(request.POST or None)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.username = form.cleaned_data['username']
            new_user.email = form.cleaned_data['email']
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            Customer.objects.create(
                user=new_user,
                phone=form.cleaned_data['phone']
            )
            user = authenticate(
                username=new_user.username, password=form.cleaned_data['password']
            )
            login(request, user)
            return HttpResponseRedirect('/')
        categories = Category.objects.get_categories_for_left_sidebar()
        context = {
            'form': form,
            'categories': categories,
            'cart': self.cart
        }
        return render(request, 'products/registration.html', context)


class ProfileView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            customer = Customer.objects.get(user=request.user)
            orders = Order.objects.filter(customer=customer).order_by('-created_at')
            categories = Category.objects.get_categories_for_left_sidebar()
            context = {
                'orders': orders,
                'cart': self.cart,
                'categories': categories,
            }
            return render(request, 'products/profile.html', context)
        else:
            raise Http404('Сторінки не існує')
