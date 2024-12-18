from django.contrib import admin
from .models import PvzLocation, Order, OrderItem, Delivery, PurchasedItem, ReturnedItem

admin.site.register(PvzLocation)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Delivery)
admin.site.register(PurchasedItem)
admin.site.register(ReturnedItem)