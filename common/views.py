from rest_framework.generics import ListAPIView,RetrieveAPIView
from .models import Region,StaticPage
from .serializers import RegionSerializer, StaticPageSerializer


class RegionListView(ListAPIView):
    queryset = Region.objects.all()
    serializer_class = RegionSerializer


class StaticPageRetrieveApiView(RetrieveAPIView):
    queryset = StaticPage.objects.all()
    serializer_class = StaticPageSerializer
