from rest_framework.generics import ListAPIView
# from django_filters.rest_framework import DjangoFilterBackend
from django_filters import rest_framework as filters
from rest_framework import filters as filter
from rest_framework.views import APIView
from .models import Product, Category
from .serializers import ProductSerializer, CategorySerializer
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from ratings.models import Rating
from rest_framework.reverse import reverse
from django.conf import settings


media_url = settings.MEDIA_URL[1:]

# Create your views here.


class ProductFilter(filters.FilterSet):
    """
    Custom filterset for ProductList View to filter results based on the
    URL parameters
    """
    category = filters.CharFilter(field_name="category__slug")
    search = filters.CharFilter(field_name="slug", lookup_expr="contains")
    min_price = filters.NumberFilter(field_name="price", lookup_expr='gte')
    max_price = filters.NumberFilter(field_name="price", lookup_expr='lte')

    class Meta:
        model = Product
        fields = ['search', 'category']


class ProductList(ListAPIView):
    """
    Returns all products by default.
    Filterset used to filter products based on the URL parameters
    """
    queryset = Product.get_products_available()
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = ProductFilter

    def list(self, request):
        base_url = reverse("shop:index", request=request)
        queryset = self.filter_queryset(Product.get_products_available())
        data = []
        try:
            if len(queryset) > 0:
                for product in queryset:
                    average_rating = Rating.get_average_rating(product=product)
                    ratings_count = Rating.get_ratings_count(product=product)
                    product_data = {
                        "id": product.id,
                        "name": product.name,
                        "slug": product.slug,
                        "price": product.price,
                        "category": product.category.name,
                        "description": product.description,
                        "image": f"{base_url}{media_url}{product.image}",
                        "rating": {"rate": average_rating, "count": ratings_count}
                    }
                    data.append(product_data)
        except Exception as e:
            # TODO: Remove for production
            print(e)
            return Response({"Can't complete this request."})

        return Response(data=data, status=status.HTTP_200_OK)


class ProductDetail(APIView):
    """
    Takes in a product id and returns the matching product if found
    """
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        base_url = reverse("shop:index", request=request)
        product_id = kwargs['id']
        try:
            product = Product.objects.get(id=product_id)
            average_rating = Rating.get_average_rating(product=product)
            ratings_count = Rating.get_ratings_count(product=product)
            all_ratings = Rating.get_all_ratings(product=product)
            product_data = {
                "id": product.id,
                "name": product.name,
                "slug": product.slug,
                "price": product.price,
                "category": product.category.name,
                "description": product.description,
                "image": f"{base_url}{media_url}{product.image}",
                "rating": {"rate": average_rating, "count": ratings_count},
                "ratings": all_ratings,
            }

        except Product.DoesNotExist:
            raise NotFound({"detail": "Product not found"})

        except Exception as e:
            # TODO: Remove for production
            print(e)
            return Response({"Can't complete this request."})

        return Response(data=product_data, status=status.HTTP_200_OK)


class CategoryList(ListAPIView):
    """Returns all categories"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]


# class ProductSearch(ListAPIView):
#     queryset = Product.get_products_available()
#     serializer_class = ProductSerializer
#     permission_classes = [AllowAny]
#     filter_backends = [filter.SearchFilter]
#     search_fields = ['slug']

#     # '^' Starts-with search
#     # '=' Exact matches
#     # '@' Full-text search. (Only supported in Django PostgreSQL)
#     # '$' Regex search
