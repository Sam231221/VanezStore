from django.contrib import admin
from .models import Category, Color,  Customer, Product, ImageAlbum, Size, ProductReview

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    exclude = ('slug',)


class ImageAlbumAdmin(admin.TabularInline):
    model = ImageAlbum
    
class ProductAdmin(admin.ModelAdmin):
    list_display =['image','title','price','category','size', 'color','is_featured','published_on','product_code']
    list_editable = ['price']
    exclude = ('slug',)
    inlines = [ImageAlbumAdmin]   
    extra = 5
    

admin.site.register(Product, ProductAdmin)    
    
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'code')     
    
admin.site.register(Customer, CustomerAdmin)


class ColorAdmin(admin.ModelAdmin):
    list_display = ('name', 'color_code')     
    
admin.site.register(Color, ColorAdmin)

admin.site.register((Size,ProductReview))


