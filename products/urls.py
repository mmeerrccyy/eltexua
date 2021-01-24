from django.urls import path
from . import views

urlpatterns = (
    path('', views.index, name='Index'),
    path('<str:ct_model>/<str:slug>/', views.ProductDetailView.as_view(), name='product_detail')
)
