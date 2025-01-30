from django.urls import path
from .views import SellerRegistrationView, LoginView, AccountMeView

urlpatterns = [
    path('seller/registration/', SellerRegistrationView.as_view(), name='seller_registration'),
    path('login/', LoginView.as_view(), name='login'),
    path('me/', AccountMeView.as_view(), name='me'),
]