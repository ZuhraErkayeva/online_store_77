from rest_framework import serializers
from products.models import Category


class AddressSerializer(serializers.Serializer):
    name = serializers.CharField()
    lat = serializers.FloatField()
    long = serializers.FloatField()


class SellerRegistrationSerializer(serializers.Serializer):
    full_name = serializers.CharField()
    project_name = serializers.CharField()
    category_id = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    phone_number = serializers.RegexField(regex=r"^\+998\d{9}$")
    address = AddressSerializer()


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class AccountsMeSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    full_name = serializers.CharField()
    phone_number = serializers.RegexField(regex=r"^\+998\d{9}$")
    profile_photo = serializers.ImageField()
    address = AddressSerializer()