from django.contrib import admin
from .models import Product, ProductImages

# Register your models here.

class ProductImagesInline(admin.TabularInline):
    model = ProductImages
    extra = 5

class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'price', 'discount_in_percent','stock', 'pubdate', 'pid', 'category']
    list_filter = ['pubdate']
    inlines = [ProductImagesInline]
    fields = ['description', 'title', 'category', 'price', 'notes','discount_in_percent','daysBeforeShipping', 'img', 'stock']
    #list_display = ['image']

admin.site.register(Product, ProductAdmin)
#admin.site.register(ProductImages, ProductImagesInline)
