from django.db import models
from django.contrib.auth import get_user_model


class Category(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title


class Brand(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)
    country = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Product(models.Model):
    vendor = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='vendor_products')
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, related_name='category_products', null=True)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='brand_products')
    price = models.DecimalField(max_digits=14, decimal_places=2)
    volume = models.PositiveIntegerField(blank=True)
    description = models.TextField(blank=True)
    available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at'])
        ]

    def __str__(self):
        return self.title


class Image(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_images')
    image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True)


class Comment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_comments')
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='user_comments')
    body = models.TextField()
    active = models.BooleanField(default=True)
    # likes_number = models.PositiveIntegerField(default=0)
    # dislikes_number = models.PositiveIntegerField(default=0)
    # stars = models.PositiveIntegerField(choices=(1, 2, 3, 4, 5))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f'Comment by {self.author.username} on {self.product.title}'

