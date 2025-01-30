from django.contrib import admin
from .models import District, StaticPage, Region


@admin.register(StaticPage)
class StaticPageAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    prepopulated_fields = {'slug': ('name', )}


class DistrictInline(admin.StackedInline):
    model = District
    extra = 0


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    inlines = [DistrictInline]