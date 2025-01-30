from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Product, Category, SubCategory, ProductImage
from common.models import District, Region
from accounts.models import Address

class CategorySerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=100)
    icon = serializers.ImageField()
    parent = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), allow_null=True, required=False)
    children = serializers.SerializerMethodField()
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    def get_children(self, obj):
        children = obj.child.all() if hasattr(obj, 'child') else obj.child_set.all()
        return CategorySerializer(children, many=True).data


    def create(self, validated_data):
        return Category.objects.create(**validated_data)


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image', 'is_main']


class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = ["id", "name"]


class DistrictSerializer(serializers.ModelSerializer):
    region = RegionSerializer()

    class Meta:
        model = District
        fields = ["id", "name", "region"]


class AddressSerializer(serializers.ModelSerializer):
    district = DistrictSerializer()

    class Meta:
        model = Address
        fields = ["district", "name", "lat", "long"]


class SubCategorySerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())

    class Meta:
        model = SubCategory
        fields = ["id", "name", "category"]


class SellerSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "full_name", "profile_photo"]


class ProductExtraSerializer(serializers.Serializer):
    is_mine = serializers.BooleanField()
    status = serializers.CharField()
    expires_at = serializers.DateField()


class ProductSerializer(serializers.ModelSerializer):
    sub_category = SubCategorySerializer()
    photos = serializers.SerializerMethodField()
    seller = SellerSerializer()
    address = serializers.SerializerMethodField()
    extra = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            "id", "name", "slug", "sub_category", "photos", "currency",
            "address", "seller", "extra"
        ]

    def get_photos(self, obj):
        return [img.image.url if img.image else None for img in obj.images.all()]


    def get_address(self, obj):
        if hasattr(obj.seller, 'address'):
            return AddressSerializer(obj.seller.address).data
        return None



    def get_extra(self, obj):
        request = self.context.get("request", None)
        return {
            "is_mine": obj.seller == request.user if request else False,
            "status": obj.status,
            "expires_at": None
        }
