from django.contrib import admin

# Register your models here.
from .models import Order, OrderProduct, Coupon, Address, Payment






class OrderAdmin(admin.ModelAdmin):
    
    list_display = ('id', 'user', 'code')
    list_display_links = ('id', 'code')
    # list_filter = ('shop', 'brand')
    # list_editable = ('is_for_sale', 'price', 'discount_price')
    search_fields = ('user__email', 'code')
    # readonly_fields = ('created_at',)
    # prepopulated_fields = {'slug':('name',)}
    list_per_page = 50

admin.site.register(Order, OrderAdmin)

admin.site.register(OrderProduct)

admin.site.register(Address)

admin.site.register(Payment)

admin.site.register(Coupon)