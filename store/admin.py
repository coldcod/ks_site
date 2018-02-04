from django.contrib import admin
from .models import Product, ProductImages

# Register your models here.

class ProductImagesInline(admin.TabularInline):
    model = ProductImages
    extra = 5

class ProductAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        if getattr(obj, 'author', None) is None:
            obj.author = request.user
        obj.save()
    def get_queryset(self, request):
        qs = super(ProductAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(author=request.user)
    #list_display = ['image']
    list_display = ['title', 'price', 'author', 'discount_in_percent','stock', 'pubdate', 'pid', 'category']
    list_filter = ['pubdate']
    inlines = [ProductImagesInline]
    fields = ['description', 'title', 'category', 'price', 'notes','discount_in_percent','daysBeforeShipping', 'img', 'stock']

admin.site.register(Product, ProductAdmin)

#admin.site.register(ProductImages, ProductImagesInline)
