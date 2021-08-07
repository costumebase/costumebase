from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from django.utils.html import mark_safe
from .models import Category, Shop, Brand, Product, Images, Color, Size, Variants, Comment


class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'vendor', 'shop', 'brand', 'category', 'name', 'image_tag', 'price', 'discount_price', 'is_for_sale')
    list_display_links = ('id', 'name')
    list_filter = ('shop', 'brand')
    list_editable = ('is_for_sale', 'price', 'discount_price')
    search_fields = ('name', 'description', 'shop__name', 'brand__name', 'vendor__user__email')
    readonly_fields = ('created_at',)
    prepopulated_fields = {'slug':('name',)}
    list_per_page = 50
admin.site.register(Product, ProductAdmin)



class CustomMPTTModelAdmin(MPTTModelAdmin):
    # specify pixel amount for this ModelAdmin only:
    mptt_level_indent = 20
    list_display = ('name','parent','id',)
    prepopulated_fields = {'slug': ('name',)} # new
admin.site.register(Category, CustomMPTTModelAdmin)



class ShopAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'image_tag', 'vendor')
    search_fields = ('name', 'vendor__user__name',)
admin.site.register(Shop, ShopAdmin)



class BrandAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
admin.site.register(Brand, BrandAdmin)



class ImagesAdmin(admin.ModelAdmin):
    list_display = ('id', 'vendor', 'product', 'image_tag',)
admin.site.register(Images, ImagesAdmin)

class ColorAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'color_tag',)
admin.site.register(Color, ColorAdmin)


class SizeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'code',)
admin.site.register(Size, SizeAdmin)



class VariantsAdmin(admin.ModelAdmin):
    model = Variants
    list_display = ('id', 'vendor', 'name', 'product', 'image_id', 'image_tag', 'size', 'price', 'quantity',)

admin.site.register(Variants, VariantsAdmin)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'user', 'subject', 'rate', 'ip', 'status', )
admin.site.register(Comment, CommentAdmin)
 