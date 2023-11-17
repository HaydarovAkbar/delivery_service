from datetime import datetime

from django.db import models
from django.contrib.auth.models import User

LEVEL = (
    ('1', 'first'),
    ('2', 'second'),
    ('3', 'third'),
    ('4', 'fourth'),
    ('5', 'fifth'),
)


class Products(models.Model):
    name_uz = models.CharField(max_length=100)
    name_ru = models.CharField(max_length=100, null=True)
    name_en = models.CharField(max_length=100, null=True)
    content_uz = models.TextField()
    content_ru = models.TextField(null=True)
    content_en = models.TextField(null=True)
    image = models.CharField(max_length=100, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.name_uz}'

    class Meta:
        db_table = 'products'
        verbose_name = 'Product'
        verbose_name_plural = 'Products'


class ProductSize(models.Model):
    name_uz = models.CharField(max_length=300)
    name_ru = models.CharField(max_length=300, null=True)
    name_en = models.CharField(max_length=300, null=True)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    status = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.name_uz}'

    class Meta:
        db_table = 'product_size'
        verbose_name = 'Product Size'
        verbose_name_plural = 'Product Sizes'


class Level(models.Model):
    title = models.CharField(max_length=100)
    count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.title}'

    abstract = True


class TGUsers(models.Model):
    fullname = models.CharField(max_length=100, null=True)
    username = models.CharField(max_length=100, unique=True, null=True)
    chat_id = models.PositiveIntegerField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    language = models.CharField(max_length=5, default='uz')
    attr = models.PositiveIntegerField(default=0)
    level = models.ForeignKey(Level, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f'{self.fullname} | {self.created_at}'

    class Meta:
        db_table = 'tg_users'
        verbose_name = 'Telegram User'
        indexes = [
            models.Index(fields=['fullname']),
            models.Index(fields=['created_at']),
            models.Index(fields=['language']),
            models.Index(fields=['attr']),
            models.Index(fields=['level']),
        ]


class TgUserLocations(models.Model):
    user = models.ForeignKey(TGUsers, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.title)

    class Meta:
        db_table = 'tg_user_locations'
        verbose_name = 'Telegram User Location'


class UserBilling(models.Model):
    user = models.ForeignKey(TGUsers, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.amount)

    class Meta:
        db_table = 'user_billing'
        verbose_name = 'User Billing'
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['created_at']),
        ]

    def save(self, *args, **kwargs):
        self.updated_at = datetime.now()
        super().save(*args, **kwargs)

    def settlement_plus(self, amount):
        self.amount += amount
        self.save()
        return self.amount

    def settlement_minus(self, amount):
        self.amount -= amount
        self.save()
        return self.amount


class BillingHistory(models.Model):
    user = models.OneToOneField(TGUsers, on_delete=models.SET_NULL, null=True)
    amount = models.DecimalField(max_digits=8, decimal_places=2, default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.amount) + ' | ' + str(self.user.fullname)

    class Meta:
        db_table = 'billing_history'
        verbose_name = 'Billing History'
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['created_at']),
        ]


class Admin(models.Model):
    chat_id = models.PositiveIntegerField(null=True)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        db_table = 'tg_admins'
        verbose_name = 'Telegram Admin'

    def __str__(self):
        return str(self.chat_id)


class Reklama(models.Model):
    title = models.TextField()
    aktiv_count = models.PositiveIntegerField(default=0)
    all_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    owner_id = models.ForeignKey(Admin, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f'{self.title}'

    class Meta:
        db_table = 'tg_reklama'
        verbose_name = 'Reklama'


class Channel(models.Model):
    title = models.CharField(max_length=100)
    url = models.URLField()
    owner_id = models.ForeignKey(Admin, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=True)
    channel_id = models.CharField(max_length=100, null=True)

    def __str__(self):
        return f'{self.title}'

    class Meta:
        db_table = 'tg_channel'
        verbose_name = 'Channel'
        verbose_name_plural = 'Channels'


class Stats(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    new_user_count = models.PositiveIntegerField(default=0)
    all_user_count = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = 'tg_stats'
        verbose_name = 'Stat'


class Feedback(models.Model):
    user = models.ForeignKey(TGUsers, on_delete=models.SET_NULL, null=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'feedback'
        indexes = [
            models.Index(fields=['user'])
        ]

    def __str__(self):
        return str(self.message)


class Caption(models.Model):
    caption = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'caption'

    def __str__(self):
        return str(self.caption)


class Message(models.Model):
    item_count = models.PositiveIntegerField(default=0)
    user = models.ForeignKey(TGUsers, on_delete=models.SET_NULL, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'message'
        verbose_name = 'Message'
        verbose_name_plural = 'Messages'
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return str(self.item_count)
