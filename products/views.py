from rest_framework import viewsets
from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer
from django.db.models import Count
from rest_framework.response import Response
from rest_framework.decorators import api_view


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer




class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.select_related("sub_category", "seller").prefetch_related("images")
    serializer_class = ProductSerializer



@api_view(['GET'])
def popular_searches(request):
    popular_products = Product.objects.annotate(
        search_count=Count('searches')
    ).order_by('-search_count')[:10].values_list('name', flat=True)

    popular_categories = Category.objects.annotate(
        search_count=Count('searches')
    ).order_by('-search_count')[:5].values_list('name', flat=True)

    return Response(list(popular_products) + list(popular_categories))

@api_view(['GET'])
def autocomplete_search(request):
    query = request.GET.get('q', '').strip()

    if not query:
        return Response([])

    product_results = Product.objects.filter(name__icontains=query).values_list('name', flat=True)[:5]
    category_results = Category.objects.filter(name__icontains=query).values_list('name', flat=True)[:3]

    return Response(list(product_results) + list(category_results))
