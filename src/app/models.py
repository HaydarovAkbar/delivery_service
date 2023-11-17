from django.db import models
from django.contrib.auth.models import User

order_status = (
    ('new', 'Yangi'),
    ('in_progress', 'Jarayonda'),
    ('delivering', 'Yetkazib berilmoqda'),
    ('completed', 'Yakunlandi'),
    ('canceled', 'Bekor qilindi')
)

_order_status_uz = {
    'new': 'Yangi 🆕',
    'in_progress': 'Jarayonda ⏳',
    'delivering': 'Yetkazib berilmoqda 🚚',
    'completed': 'Yakunlandi ✅',
    'canceled': 'Bekor qilindi ❌'
}

_order_status_ru = {
    'new': 'Новый 🆕',
    'in_progress': 'В процессе ⏳',
    'delivering': 'Доставляется 🚚',
    'completed': 'Завершен ✅',
    'canceled': 'Отменен ❌'
}


class Category(models.Model):
    name_uz = models.CharField(max_length=100)
    name_ru = models.CharField(max_length=100)
    image_uz = models.CharField(max_length=100)
    image_ru = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.name_uz}'

    class Meta:
        db_table = 'category'
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class Products(models.Model):
    name_uz = models.CharField(max_length=100)
    name_ru = models.CharField(max_length=100)
    content_uz = models.TextField()
    content_ru = models.TextField()
    price = models.PositiveIntegerField()
    discount = models.PositiveIntegerField(default=0)
    image = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name_uz}'

    class Meta:
        db_table = 'products'
        verbose_name = 'Product'
        verbose_name_plural = 'Products'


class ProductSize(models.Model):
    name_uz = models.CharField(max_length=100)
    name_ru = models.CharField(max_length=100)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    price = models.PositiveIntegerField()
    discount = models.PositiveIntegerField(default=0)
    status = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.name_uz}'

    class Meta:
        db_table = 'product_size'
        verbose_name = 'Product Size'
        verbose_name_plural = 'Product Sizes'


class TGUsers(models.Model):
    fullname = models.CharField(max_length=100, null=True)
    username = models.CharField(max_length=100, unique=True, null=True)
    phone_number = models.CharField(max_length=14, null=True)
    chat_id = models.PositiveIntegerField(null=True)
    date_of_created = models.DateTimeField(auto_now_add=True)
    language = models.CharField(max_length=3, default='uz')

    def __str__(self):
        return f'{self.fullname} | {self.date_of_created}'

    class Meta:
        db_table = 'tg_users'
        verbose_name = 'Telegram User'


class TgUserLocations(models.Model):
    user = models.ForeignKey(TGUsers, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    latitude = models.CharField(max_length=100)
    longitude = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.title)

    class Meta:
        db_table = 'tg_user_locations'
        verbose_name = 'Telegram User Location'


class Admin(models.Model):
    user_id = models.PositiveIntegerField(null=True)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        db_table = 'tg_admins'
        verbose_name = 'Telegram Admin'

    def __str__(self):
        return str(self.user_id)


class Reklama(models.Model):
    title = models.TextField()
    aktiv_count = models.PositiveIntegerField(default=0)
    all_count = models.PositiveIntegerField(default=0)
    date_of_created = models.DateTimeField(auto_now_add=True)
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
    date_of_created = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=True)
    channel_id = models.CharField(max_length=100, null=True)

    def __str__(self):
        return f'{self.title}'

    class Meta:
        db_table = 'tg_channel'
        verbose_name = 'Channel'
        verbose_name_plural = 'Channels'


class Stats(models.Model):
    date_of_created = models.DateTimeField(auto_now_add=True)
    new_user_count = models.PositiveIntegerField(default=0)
    all_user_count = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = 'tg_stats'
        verbose_name = 'Stat'


class Feedback(models.Model):
    sender_name = models.CharField(max_length=200)
    sender_id = models.PositiveIntegerField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'feedback'
        indexes = [
            models.Index(fields=['sender_id'])
        ]

    def __str__(self):
        return str(self.sender_name)


class Caption(models.Model):
    caption = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'caption'

    def __str__(self):
        return str(self.caption)


class Supplier(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=14)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False)
    chat_id = models.PositiveIntegerField(null=True)
    owner_id = models.ForeignKey(Admin, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return str(self.name)

    class Meta:
        db_table = 'supplier'


class SupplierPrice(models.Model):
    price = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'supplier_price'

    def __str__(self):
        return str(self.price)


class Order(models.Model):
    user = models.ForeignKey(TGUsers, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True, null=True)
    status = models.CharField(max_length=100, default='new', choices=order_status)
    delivery_price = models.PositiveIntegerField(default=0)
    total_price = models.PositiveIntegerField(default=0)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, null=True)
    location = models.ForeignKey(TgUserLocations, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return str(self.user)

    class Meta:
        db_table = 'order'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product_size = models.ForeignKey(ProductSize, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Products, on_delete=models.CASCADE, null=True)
    count = models.PositiveIntegerField(default=1)
    price = models.PositiveIntegerField(default=0)
    total_price = models.PositiveIntegerField(default=0)

    def __str__(self):
        return str(self.product)

    class Meta:
        db_table = 'order_item'
        verbose_name = 'Order Item'
        verbose_name_plural = 'Order Items'


class OrderAddress(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    user = models.ForeignKey(TGUsers, on_delete=models.CASCADE, null=True, blank=True)
    address = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.address)

    class Meta:
        db_table = 'order_address'
        verbose_name = 'Order Address'
        verbose_name_plural = 'Order Addresses'


class Boss(models.Model):
    user_id = models.PositiveIntegerField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user_id)

    class Meta:
        db_table = 'boss'
        verbose_name = 'Boss'
        verbose_name_plural = 'Bosses'
