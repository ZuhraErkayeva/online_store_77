from django.urls import path
from . import views


urlpatterns = [
    path('regions-with-districts/', views.RegionListView.as_view(), name='regions'),
    path('static_page/<int:pk>/', views.StaticPageRetrieveApiView.as_view(), name='static_page'),
]