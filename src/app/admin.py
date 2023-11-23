from django.contrib import admin
from .models import TGUsers, Channel, Admin, Reklama, Stats, Products, Caption, ProductSize, Level


class AdminProduct(admin.ModelAdmin):
    list_display = ('name', 'price', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('name', 'price')
    list_per_page = 10


admin.site.register(TGUsers)
admin.site.register(Channel)
admin.site.register(Admin)
admin.site.register(Reklama)
admin.site.register(Stats)
admin.site.register(Products)
admin.site.register(Caption)
admin.site.register(ProductSize)
admin.site.register(Level)