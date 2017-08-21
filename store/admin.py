from django.contrib import admin
from .models import Product, ProductImages

# Register your models here.

class ProductImagesInline(admin.TabularInline):
    model = ProductImages
    extra = 5

class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'price', 'stock', 'pubdate', 'pid']
    list_filter = ['pubdate']
    inlines = [ProductImagesInline]
    fields = ['description', 'title', 'price', 'daysBeforeShipping', 'img', 'stock']
    #list_display = ['image']

admin.site.register(Product, ProductAdmin)
#admin.site.register(ProductImages, ProductImagesInline)
