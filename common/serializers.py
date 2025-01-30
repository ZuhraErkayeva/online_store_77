from rest_framework import serializers


class DistrictSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()


class RegionSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    districts = DistrictSerializer(many=True)


class StaticPageSerializer(serializers.Serializer):
    slug = serializers.SlugField()
    content = serializers.CharField()
