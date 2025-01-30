
from .views import CategoryViewSet, ProductViewSet
from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import popular_searches, autocomplete_search


router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')
router.register(r'categories', CategoryViewSet, basename='category')

urlpatterns = [
    path('store/search/populars', popular_searches),
    path('store/search/complete', autocomplete_search),
] + router.urls
