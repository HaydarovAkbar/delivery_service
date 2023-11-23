from django.contrib import admin
from .models import TGUsers, Channel, Admin, Reklama, Stats, Products, Caption, ProductSize, Level
from modeltranslation.admin import TranslationAdmin


class ProductTranslate(TranslationAdmin):
    fieldsets = (
        ('Uz', {'fields': ('name_uz', 'content_uz')}),
        ('Eng', {'fields': ('name_en', 'content_en')}),
        ('Ru', {'fields': ('name_ru', 'content_ru')}),
        ('Image', {'fields': ('image',)}),
        ('Status', {'fields': ('status',)}),
    )
    search_fields = ('name_uz', 'name_en', 'name_ru')
    list_per_page = 10
    list_filter = ('created_at', 'updated_at')


class ProductSizeTranslate(TranslationAdmin):
    list_display = ('name', 'product', 'status')
    list_filter = ('status',)
    search_fields = ('name_uz',)
    list_per_page = 10
    fieldsets = (
        ('Uz', {'fields': ('name_uz',)}),
        ('Eng', {'fields': ('name_en',)}),
        ('Ru', {'fields': ('name_ru',)}),
        ('Product', {'fields': ('product',)}),
        ('Status', {'fields': ('status',)}),
    )


class AdminFilter(admin.ModelAdmin):
    search_fields = ('fullname',)
    list_per_page = 15


admin.site.register(TGUsers, AdminFilter)
admin.site.register(Channel)
admin.site.register(Admin)
admin.site.register(Reklama)
admin.site.register(Stats)
admin.site.register(Products, ProductTranslate)
admin.site.register(Caption)
admin.site.register(ProductSize, ProductSizeTranslate)
admin.site.register(Level)
