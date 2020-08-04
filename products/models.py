from django.conf import settings 
from django.db import models
from django.db.models import Sum
from django.shortcuts import reverse
from django_countries.fields import CountryField
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.utils.text import slugify
import string
import random

CATEGORY_CHOICES = (
        ('PH', 'PHONES'),
        ('LT', 'LAPTOPS'),
        ('C', 'COMPUTERS'),
        ('T', 'TABLES'),
    )
ADDRESS_CHOICES = (
    ('B', 'Billing'),
    ('S', 'Shiping'),
    )

class Slide(models.Model):
    caption1 = models.CharField(max_length=100)
    caption2 = models.CharField(max_length=100)
    link = models.CharField(max_length=100)
    image = models.ImageField(upload_to='media',help_text ='Image')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return "{} - {}".format(self.caption1, self.caption2)
    
class Category(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField()
    description = models.TextField()
    image = models.ImageField()
    is_Active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        title = self.title
        self.slug = sligify(title, allow_unicode=True)
        super().save(*args, **kwargs)

class Product(models.Model):
    title = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    slug = models.SlugField(blank=True)
    description = models.CharField(max_length=300)
    image = models.ImageField(upload_to='media')
    price = models.DecimalField(max_digits=5, decimal_places=2)
    discount = models.DecimalField(max_digits=4, decimal_places=2,blank=True)

    def __str__(self):
        return self.title

    def total_price(self):
        return self.price - self.discount

    def get_absolute_url(self):
        return reverse("Product", kwargs = {'slug': self.slug})
    
    def add_to_cart_url(self):
        return reverse("products:add-to-cart", kwargs={'slug': self.slug})
  
    def remove_from_cart_url(self):
        return reverse("products:remove-from-cart", kwargs={'slug': self.slug})
    
    def slug_string_generator(self):
        chars = string.ascii_lowercase + string.digits
        slug_string = ''.join(random.choice(chars) for i in range(10))
        return slug_string
    
    def save(self, *args, **kwargs):
        title = self.title
        id = self.id
        slug_string = slug_string_generator()
        self.slug = slugify(f'{title}{slug_string}', allow_unicode=True)
        super().save(*args, **kwargs)
        

#@receiver(post_save, sender=Product)
#def generate_slug(sender, created, *args, **kwargs):
    #if created:
       #slug = slug_generator(sender)
       #slug.save()




class Ordered_Product(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.item.title}"

    def total_price(self):
        return self.quantity * self.product.price

    def discount_price(self):
        return self.quantity * self.product.discount

    def tolal_price(self):
        if self.product.discount:
            return self.discount_price
        return self.total_price

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    items = models.ManyToManyField(Ordered_Product)
    ordered_date = models.DateTimeField(auto_now_add=True)
    address = models.ForeignKey('Address', on_delete=models.SET_NULL, blank=True, null=True)
    deal_end = models.DateTimeField()
    payment = models.ForeignKey('Payment', on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.user.username

    def get_total(self):
        total = 0
        for ordered_product in self.items.all():
            total = total + ordered_product.total_price()

class Address(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    street = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    country = CountryField()
    
    def __str__(self):
        return self.user.username

class Payment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)
    money = models.DecimalField(max_digits=5, decimal_places=2)