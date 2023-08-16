from django.contrib import admin

from .models import Customer, Product, Cart, OrderPlaced

# Register your models here.
# admin.site.register(Customer)
@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'locality', 'city', 'zipcode', 'state')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'brand', 'category', 'selling_price', 'discounted_price')

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'product', 'quantity')    

@admin.register(OrderPlaced)
class OrderPlacedAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'product', 'customer', 'quantity', 'ordered_date', 'status')    