from django.contrib import admin
from .models import DeliveryOptions, BillingAddress, Order, OrderItem
# Register your models here.
admin.site.register(DeliveryOptions)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(BillingAddress)