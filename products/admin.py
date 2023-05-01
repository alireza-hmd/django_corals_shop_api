from django.contrib import admin
from .models import Product, Brand, Category, Image, Comment


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug')


class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'brand', 'price', 'available', 'created_at')
    list_filter = ('category', 'available', 'created_at')
    list_editable = ('price', 'available')


class BrandAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'country')


class ImageAdmin(admin.ModelAdmin):
    list_display = ('image', 'product')


class CommentAdmin(admin.ModelAdmin):
    list_display = ('product', 'author', 'active', 'created_at')
    list_filter = ('active', 'created_at')
    search_fields = ('body',)
    list_editable = ('active',)


admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Brand, BrandAdmin)
admin.site.register(Image, ImageAdmin)
admin.site.register(Comment, CommentAdmin)