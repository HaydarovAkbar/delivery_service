from django.utils.translation import gettext_lazy as _
from modeltranslation.translator import TranslationOptions, register

from app.models import Products, ProductSize, TGUsers, Level


@register(Products)
class ProductsTranslationOptions(TranslationOptions):
    fields = ('name', 'content', )


@register(ProductSize)
class ProductSizeTranslationOptions(TranslationOptions):
    fields = ('name', )