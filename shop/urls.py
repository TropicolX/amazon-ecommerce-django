from django.urls import path
from .views import ProductList, ProductDetail, CategoryList
from django.views.generic import TemplateView

app_name = "shop"

urlpatterns = [
    path('', TemplateView.as_view(template_name="shop/index.html"), name="index"),
    path('api/products/', ProductList.as_view(), name="product_list"),
    path('api/products/<int:id>/', ProductDetail.as_view(), name="product_detail"),
    path('api/categories/', CategoryList.as_view(), name="category_list"),
]
