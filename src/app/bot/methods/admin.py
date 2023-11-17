from telegram import Update, ReplyKeyboardRemove
from telegram.ext import CallbackContext
from app.bot.states import States as state
from app.bot.messages.main import MessageText as msg_text
from app.models import Admin, TGUsers, Channel, Category, Products, Supplier, Order, OrderItem, OrderAddress, \
    order_status, ProductSize, _order_status_uz
from django.db.models import Q
from app.bot.keyboards.base import Keyboards as kb, number as num


def admin(update: Update, context: CallbackContext):
    admin_id = update.effective_user.id
    admin_db = Admin.objects.filter(user_id=admin_id)
    if admin_db:
        update.message.reply_html(msg_text.is_admin.get('uz'), reply_markup=kb.admin('uz'))
        return state.admin


def bot_users(update: Update, context: CallbackContext):
    count = TGUsers.objects.all().count()
    last_50 = TGUsers.objects.all().order_by('-date_of_created')[:50]
    msg = f"Bot foydalanuvchilari soni: {count}\n\n"
    for user in last_50:
        msg += f"{user.id}) {user.fullname} | {user.date_of_created.strftime('%d.%m.%Y')}\n"
    update.message.reply_text(msg, reply_markup=kb.back('uz'))
    update.message.reply_html(msg_text.search_user.get('uz'), reply_markup=kb.back('uz'))
    return state.search_user


def search_user(update: Update, context: CallbackContext):
    users = TGUsers.objects.filter(fullname__icontains=update.message.text)
    if users:
        msg = f"Botdagi natijalari soni: {users.count()}\n\n"
        for user in users:
            msg += f"{user.id}) {user.fullname} | {user.date_of_created.strftime('%d.%m.%Y')}\n"
        update.message.reply_text(msg, reply_markup=kb.back('uz'))
    else:
        update.message.reply_html(msg_text.not_found_user.get('uz'), reply_markup=kb.back('uz'))
    return state.admin


def channel(update: Update, context: CallbackContext):
    channels = Channel.objects.all()
    msg_text = "Sizga tegishli kanallar ro'yxati:\n\n"
    for channel in channels:
        msg_text += f"{channel.id}) {channel.title} | {channel.url} | {channel.channel_id} | {channel.status}\n"
    update.message.reply_text(msg_text, reply_markup=kb.back('uz'))
    return state.channel_set


def channel_add(update: Update, context: CallbackContext):
    update.message.reply_html(msg_text.enter_channel_title.get('uz'), reply_markup=kb.back('uz'))
    return state.channel_add_title


def channel_add_title(update: Update, context: CallbackContext):
    title = update.message.text
    context.user_data['title'] = title
    update.message.reply_html(msg_text.enter_channel_url.get('uz'), reply_markup=kb.back('uz'))
    return state.channel_add_url


def channel_add_url(update: Update, context: CallbackContext):
    url = update.message.text
    context.user_data['url'] = url
    update.message.reply_html(msg_text.enter_channel_id.get('uz'), reply_markup=kb.back('uz'))
    return state.channel_add_id


def channel_add_id(update: Update, context: CallbackContext):
    channel_id = update.message.text
    context.user_data['channel_id'] = channel_id
    title = context.user_data['title']
    url = context.user_data['url']
    channel_id = context.user_data['channel_id']
    admin_id = update.effective_user.id
    admin_db = Admin.objects.get(user_id=admin_id)
    Channel.objects.create(title=title, url=url, channel_id=channel_id, owner_id=admin_db)
    update.message.reply_html(msg_text.succesfuly_added.get('uz'), reply_markup=kb.admin('uz'))
    return state.admin


def channel_one_set(update: Update, context: CallbackContext):
    channel_number = update.message.text
    if not channel_number.isdigit():
        update.message.reply_text('Siz raqam kiritmadingiz!!!')
        return state.channel_one_set
    try:
        channel = Channel.objects.get(id=channel_number)
    except Channel.DoesNotExist:
        update.message.reply_text('Bunday raqamli kanal mavjud emas!!!')
        return state.channel_set_one
    msg_txt = f"Kanal nomi: {channel.title}\nKanal havolasi: {channel.url}\nKanal ID: {channel.channel_id}\nKanal statusi: {channel.status} \n\n nimani o'zgartirmoqchisiz ?"
    context.user_data['channel_id'] = channel.id
    update.message.reply_text(msg_txt, reply_markup=kb.channel_one_set('uz'))
    return state.channel_set_one


def channel_one_set_status(update: Update, context: CallbackContext):
    channel = Channel.objects.get(id=context.user_data['channel_id'])
    if channel.status:
        channel.status = False
        channel.save()
        update.message.reply_text('Kanal o\'chirildi')
    else:
        channel.status = True
        channel.save()
        update.message.reply_text('Kanal yoqildi')
    return state.channel_set_one


def get_adm_stats(update: Update, context: CallbackContext):
    update.message.reply_text('Admin statistikasi')
    return state.admin


def admin_back(update: Update, context: CallbackContext):
    user = Admin.objects.filter(user_id=update.effective_user.id)
    if user:
        update.message.reply_html(msg_text.is_admin.get('uz'), reply_markup=kb.admin('uz'))
        return state.admin


def channel_del(update: Update, context: CallbackContext):
    channel_number = update.message.text
    if not channel_number.isdigit():
        update.message.reply_text('Siz raqam kiritmadingiz!!!')
        return state.channel_one_set
    try:
        channel = Channel.objects.get(id=channel_number)
    except Channel.DoesNotExist:
        update.message.reply_text('Bunday raqamli kanal mavjud emas!!!')
        return state.channel_set_one
    msg_txt = f"Kanal nomi: {channel.title}\nKanal havolasi: {channel.url}\nKanal ID: {channel.channel_id}\nKanal statusi: {channel.status} \n\n O'chiriladi"
    channel.delete()
    update.message.reply_text(msg_txt, reply_markup=kb.channel_deleted('uz'))
    return state.channel_set_one


def add_category(update: Update, context: CallbackContext):
    """Add category to project"""
    update.message.reply_text(msg_text.add_category.get('uz'))
    return state.add_category


def get_category(update: Update, context: CallbackContext):
    """Get category from user"""
    msg = update.message.text
    if '*' not in msg:
        update.message.reply_text('Siz xato kiritdingiz!!! \n\n Masalan: Lavash * Лаваш')
        return state.add_category
    uz, ru = msg.split('*')
    uz = uz.strip()
    ru = ru.strip()
    context.user_data['uz'] = uz
    context.user_data['ru'] = ru
    update.message.reply_text(msg_text.add_category_image_uz.get('uz'),
                              reply_markup=kb.back('uz'))
    return state.category_image_uz


def get_category_image_uz(update: Update, context: CallbackContext):
    """Get category image from user"""
    photo = update.message.photo[-1].file_id
    context.user_data['image_uz'] = photo
    update.message.reply_text(msg_text.add_category_image_ru.get('uz'),
                              reply_markup=kb.back('uz'))
    return state.category_image_ru


def get_category_image_ru(update: Update, context: CallbackContext):
    """Get category image from user"""
    photo = update.message.photo[-1].file_id
    uz = context.user_data['uz']
    ru = context.user_data['ru']
    image_uz = context.user_data['image_uz']
    Category.objects.create(name_uz=uz, name_ru=ru, image_uz=image_uz, image_ru=photo)
    update.message.reply_html(msg_text.succesfuly_added.get('uz'), reply_markup=kb.admin('uz'))
    return state.admin


def all_category(update: Update, context: CallbackContext):
    """Get all category from database"""
    categories = Category.objects.all()
    if not categories:
        update.message.reply_text('Kategoriyalar mavjud emas!!!')
        return state.admin
    msg = "Barcha kategoriyalar ro'yxati:\n\n"
    for category in categories:
        msg += f"{category.id}) {category.name_uz} | {category.name_ru}\n"
    update.message.reply_text(msg, reply_markup=kb.back('uz'))
    return state.del_category


def category_del(update: Update, context: CallbackContext):
    category_number = update.message.text
    if not category_number.isdigit():
        update.message.reply_text('Siz raqam kiritmadingiz!!!')
        return state.del_category
    try:
        category = Category.objects.get(id=category_number)
    except Category.DoesNotExist:
        update.message.reply_text('Bunday raqamli kategoriya mavjud emas!!!')
        return state.del_category
    msg_txt = f"Kategoriya nomi: {category.name_uz}\nKategoriya nomi: {category.name_ru}\n\n O'chiriladi"
    category.delete()
    update.message.reply_text(msg_txt, reply_markup=kb.admin('uz'))
    return state.admin


def add_product(update: Update, context: CallbackContext):
    """Add product to project"""
    update.message.reply_text(msg_text.add_product_name.get('uz'), reply_markup=kb.back('uz'))
    return state.add_product


def get_product_name(update: Update, context: CallbackContext):
    """Get product name from user"""
    msg = update.message.text
    if '*' not in msg:
        update.message.reply_text('Siz xato kiritdingiz!!! \n\n Masalan: Lavash sirli * Лаваш сырный')
        return state.add_product
    uz, ru = msg.split('*')
    uz = uz.strip()
    ru = ru.strip()
    context.user_data['name_uz'] = uz
    context.user_data['name_ru'] = ru
    update.message.reply_text(msg_text.add_product_content.get('uz'), reply_markup=kb.back('uz'))
    return state.add_product_content


def get_product_content(update: Update, context: CallbackContext):
    """Get product content from user"""
    msg = update.message.text
    if '*' not in msg:
        update.message.reply_text('Siz xato kiritdingiz!!! \n\n Masalan: Lavash sirli * Лаваш сырный')
        return state.add_product
    uz, ru = msg.split('*')
    uz = uz.strip()
    ru = ru.strip()
    context.user_data['content_uz'] = uz
    context.user_data['content_ru'] = ru
    update.message.reply_text(msg_text.add_product_price.get('uz'), reply_markup=kb.back('uz'))
    return state.add_product_price


def add_product_price(update: Update, context: CallbackContext):
    """Get product price from user"""
    msg = update.message.text
    if not msg.isdigit():
        update.message.reply_text('Siz xato kiritdingiz!!! \n\n Masalan: 10000')
        return state.add_product_price
    context.user_data['price'] = msg
    update.message.reply_text(msg_text.add_product_discount.get('uz'), reply_markup=kb.back('uz'))
    return state.add_product_discount


def add_product_discount(update: Update, context: CallbackContext):
    """Get product discount from user"""
    msg = update.message.text
    if not msg.isdigit():
        update.message.reply_text('Siz xato kiritdingiz!!! \n\n Masalan: 9990')
        return state.add_product_discount
    context.user_data['discount'] = msg
    update.message.reply_text(msg_text.add_product_photo.get('uz'), reply_markup=kb.back('uz'))
    return state.add_product_photo


def add_product_photo(update: Update, context: CallbackContext):
    """Get product photo from user"""
    image = update.message.photo[-1].file_id
    context.user_data['image'] = image
    all_category = Category.objects.all()
    update.message.reply_text(msg_text.add_product_category.get('uz'), reply_markup=kb.category_list(all_category))
    return state.add_product_category


def add_product_category(update: Update, context: CallbackContext):
    """Get product category from user"""
    query = update.callback_query
    category_id = query.data
    category = Category.objects.get(id=category_id)
    uz_name = context.user_data['name_uz']
    ru_name = context.user_data['name_ru']
    uz_content = context.user_data['content_uz']
    ru_content = context.user_data['content_ru']
    price = context.user_data['price']
    discount = context.user_data['discount']
    image = context.user_data['image']
    msg = Products.objects.create(name_uz=uz_name, name_ru=ru_name, content_uz=uz_content, content_ru=ru_content,
                                  price=price, discount=discount, image=image, category=category)
    query.delete_message()
    context.user_data['add_product'] = msg
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text='Mahsulot muvaffaqiyatli qo\'shildi!!! \n\n' + msg_text.product_devided_size.get(
                                 'uz'),
                             reply_markup=kb.yes_no('uz'))
    return state.product_yes_no


def product_no_size(update: Update, context: CallbackContext):
    update.message.reply_text('Mahsulot muvaffaqiyatli qo\'shildi!!!', reply_markup=kb.admin('uz'))
    return state.admin


def product_yes_size(update: Update, context: CallbackContext):
    update.message.reply_text('Mahsulot muvaffaqiyatli qo\'shildi!!! \n\n' + msg_text.product_size_name.get('uz'),
                              reply_markup=kb.back('uz'))
    return state.product_size_name


def product_size_name(update: Update, context: CallbackContext):
    msg = update.message.text
    if '*' not in msg:
        update.message.reply_text('Siz xato kiritdingiz!!! \n\n Masalan: Lavash sirli * Лаваш сырный')
        return state.product_size_name
    uz, ru = msg.split('*')
    uz = uz.strip()

    ru = ru.strip()
    context.user_data['size_name_uz'] = uz
    context.user_data['size_name_ru'] = ru
    update.message.reply_text(msg_text.product_size_price.get('uz'), reply_markup=kb.back('uz'))
    return state.product_size_price


def product_size_price(update: Update, context: CallbackContext):
    msg = update.message.text
    if not msg.isdigit():
        update.message.reply_text('Siz xato kiritdingiz!!! \n\n Masalan: 10000')
        return state.product_size_price
    ProductSize.objects.create(name_uz=context.user_data['size_name_uz'], name_ru=context.user_data['size_name_ru'],
                               price=msg, product=context.user_data['add_product'])
    update.message.reply_text(msg_text.add_again.get('uz') + '\n\n' + msg_text.product_size_name.get('uz'),
                              reply_markup=kb.back('uz'))
    return state.product_size_name


def all_product(update: Update, context: CallbackContext):
    """Get all product from database"""
    products = Products.objects.all()[::-1]
    if not products:
        update.message.reply_text('Mahsulotlar mavjud emas!!!')
        return state.admin
    msg = "Barcha mahsulotlar ro'yxati:\n\n"
    for product in products[:30]:
        msg += f"{product.id}) {product.name_uz} | {product.price} | {product.discount}\n"
    update.message.reply_text(msg, reply_markup=kb.back('uz'))
    return state.del_product


def product_del(update: Update, context: CallbackContext):
    product_number = update.message.text
    if not product_number.isdigit():
        update.message.reply_text('Siz raqam kiritmadingiz!!!')
        return state.del_product
    try:
        product = Products.objects.get(id=product_number)
    except Products.DoesNotExist:
        update.message.reply_text('Bunday raqamli mahsulot mavjud emas!!!')
        return state.del_product
    msg_txt = f"Mahsulot nomi: {product.name_uz}\nMahsulot narxi: {product.price}\nMahsulot chegirma narxi: {product.discount} \n\n O'chiriladi"
    product.delete()
    update.message.reply_text(msg_txt, reply_markup=kb.admin('uz'))
    return state.admin


def add_admin(update: Update, context: CallbackContext):
    """Add admin to project"""
    update.message.reply_text(msg_text.add_admin_with_chat_id.get('uz'), reply_markup=kb.back('uz'))
    return state.add_admin


def get_admin_chat_id(update: Update, context: CallbackContext):
    """Get admin chat id from user"""
    chat_id = update.message.text
    if not chat_id.isdigit():
        update.message.reply_text('Siz raqam kiritmadingiz!!!')
        return state.add_admin
    Admin.objects.create(user_id=chat_id)
    update.message.reply_text('Admin muvaffaqiyatli qo\'shildi', reply_markup=kb.admin('uz'))
    return state.admin


def all_admin(update: Update, context: CallbackContext):
    """Get all admin from database"""
    admins = Admin.objects.all()
    msg = "Barcha adminlar ro'yxati:\n\n"
    for admin in admins:
        msg += f"{admin.id}) {admin.user_id} | {admin.created_at.strftime('%d.%m.%Y')}\n"
    update.message.reply_text(msg, reply_markup=kb.back('uz'))
    return state.del_admin


def admin_del(update: Update, context: CallbackContext):
    """Delete admin from database"""
    admin_number = update.message.text
    if not admin_number.isdigit():
        update.message.reply_text('Siz raqam kiritmadingiz!!!')
        return state.del_admin
    try:
        admin = Admin.objects.get(id=admin_number)
    except Admin.DoesNotExist:
        update.message.reply_text('Bunday raqamli admin mavjud emas!!!')
        return state.del_admin
    msg_txt = f"Admin chat id: {admin.user_id}\n\n O'chiriladi"
    admin.delete()
    update.message.reply_text(msg_txt, reply_markup=kb.admin('uz'))
    return state.admin


def add_supplier(update: Update, context: CallbackContext):
    """Add supplier to project"""
    update.message.reply_text(msg_text.add_supplier_with_chat_id.get('uz'), reply_markup=kb.back('uz'))
    return state.add_supplier


def get_supplier_chat_id(update: Update, context: CallbackContext):
    """Get supplier chat id from user"""
    chat_id = update.message.text
    if not chat_id.isdigit():
        update.message.reply_text('Siz raqam kiritmadingiz!!!')
        return state.add_supplier
    context.user_data['supplier_chat_id'] = chat_id
    update.message.reply_text(msg_text.add_supplier_name.get('uz'), reply_markup=kb.back('uz'))
    return state.add_supplier_name


def get_supplier_name(update: Update, context: CallbackContext):
    """Get supplier name from user"""
    name = update.message.text
    context.user_data['supplier_name'] = name
    update.message.reply_text(msg_text.add_supplier_phone.get('uz'), reply_markup=kb.back('uz'))
    return state.add_supplier_phone


def get_supplier_phone(update: Update, context: CallbackContext):
    """Get supplier phone from user"""
    phone = update.message.text
    chat_id = context.user_data['supplier_chat_id']
    name = context.user_data['supplier_name']
    admin_id = update.effective_user.id
    admin_db = Admin.objects.get(user_id=admin_id)
    Supplier.objects.create(name=name, phone=phone, chat_id=chat_id, owner_id=admin_db, status=True)
    update.message.reply_text('Taminotchi muvaffaqiyatli qo\'shildi', reply_markup=kb.admin('uz'))
    return state.admin


def all_supplier(update: Update, context: CallbackContext):
    """Get all supplier from database"""
    suppliers = Supplier.objects.all()
    if not suppliers:
        update.message.reply_text('Taminotchilar mavjud emas!!!')
        return state.admin
    msg = "Barcha taminotchilar ro'yxati:\n\n"
    for supplier in suppliers:
        msg += f"{supplier.id}) {supplier.name} | {supplier.phone} | {supplier.status}\n"
    update.message.reply_text(msg, reply_markup=kb.back('uz'))
    return state.del_supplier


def supplier_del(update: Update, context: CallbackContext):
    """Delete supplier from database"""
    supplier_number = update.message.text
    if not supplier_number.isdigit():
        update.message.reply_text('Siz raqam kiritmadingiz!!!')
        return state.del_supplier
    try:
        supplier = Supplier.objects.get(id=supplier_number)
    except Supplier.DoesNotExist:
        update.message.reply_text('Bunday raqamli taminotchi mavjud emas!!!')
        return state.del_supplier
    msg_txt = f"Taminotchi nomi: {supplier.name}\nTaminotchi telefon raqami: {supplier.phone}\n\n O'chiriladi"
    supplier.delete()
    update.message.reply_text(msg_txt, reply_markup=kb.admin('uz'))
    return state.admin


def adversting(update: Update, context: CallbackContext):
    """Send adversting to all users"""
    update.message.reply_text(msg_text.send_adversting.get('uz'), reply_markup=kb.back('uz'))
    return state.adversting


def get_adversting(update: Update, context: CallbackContext):
    """Get adversting from user"""
    users = TGUsers.objects.all()
    all_count = users.count()
    update.message.reply_text('Reklama yuborilmoqda...')
    c = 0
    for user in users:
        try:
            update.message.copy(chat_id=user.chat_id)
            c += 1
        except:
            pass
    msg = f"Reklama {c} ta foydalanuvchiga yuborildi \n\nJami foydalanuvchilar soni: {all_count}"
    update.message.reply_text(msg, reply_markup=kb.admin('uz'))
    return state.admin


def get_unfinished_orders(update: Update, context: CallbackContext):
    """Get unfinished orders from database"""
    orders = Order.objects.filter(Q(status='new') | Q(status='delivering') | Q(status='in_progress'))
    if not orders:
        update.message.reply_text('Tugatilmagan buyurtmalar mavjud emas!!!')
        return state.admin
    msg = "Tugatilmagan buyurtmalar ro'yxati:\n\n"
    for order in orders[::-1][:20]:
        msg += f"{order.id}) {order.user.fullname} | {order.total_price} | {order.created_at.strftime('%d.%m.%Y %H:%M')}\n"
    update.message.reply_text(msg, reply_markup=kb.back('uz'))
    return state.unfinished_orders


def get_order_id(update: Update, context: CallbackContext):
    order_id = update.message.text
    if not order_id.isdigit():
        update.message.reply_text('Siz raqam kiritmadingiz!!!')
        return state.unfinished_orders
    try:
        order = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        update.message.reply_text('Bunday raqamli buyurtma mavjud emas!!!')
        return state.unfinished_orders
    context.user_data['order_id'] = order.id
    msg = (f"<b>Buyurtma haqida ma'lumot</b>\n\n"
           f"🆔 Buyurtma ID: #{order.id}"
           f"\n🔹 Buyurtma holati: {_order_status_uz.get(order.status)}\n"
           f"👤 Buyurtma egasi: {order.user.fullname}"
           f"\n☎️ Buyurtma telefon raqami: {order.user.phone_number}"
           f"\n📍 Buyurtma manzili: {order.location.title}"
           f"\n🕔 Buyurtma yaratilgan vaqti: {order.created_at.strftime('%d.%m.%Y %H:%M')}"
           f"\n🕔 Buyurtma yangilangan vaqti: {order.update_at.strftime('%d.%m.%Y %H:%M')}"
           f"\n\n➡️ kimga biriktirmoqchisiz tanlang !!!")
    msg += f"    <b>🛍 Buyurtma mahsulotlari:</b>\n\n"
    for item in OrderItem.objects.filter(order=order):
        msg += f"📦 Mahsulot: <b>{item.product_size.name_uz} - {item.product.name_uz}</b>\n" \
               f"📝 Narxi: <b>{num(item.product.price)}</b> so'm\n" \
               f"📝 Soni: <b>{item.count}</b>\n" \
               f"💰 Umumiy summa: <b>{num(item.total_price)}</b> so'm\n\n"
    update.message.reply_html(msg, reply_markup=ReplyKeyboardRemove())
    supplier_list = Supplier.objects.filter(status=True)
    update.message.reply_text(msg_text.all_supplier.get('uz'), reply_markup=kb.supplier_list(supplier_list))
    return state.choose_order_supplier


def choose_order_supplier(update: Update, context: CallbackContext):
    query = update.callback_query
    supplier_id = query.data
    if query.data == 'cencel':
        query.delete_message()
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text='Buyurtma muvaffaqiyatli bekor qilindi!!!',
                                 reply_markup=kb.admin('uz'))
        return state.admin
    elif query.data == 'back':
        query.delete_message()
        context.bot.send_message(chat_id=update.effective_chat.id, text='Admin panelga qaytdik',
                                 reply_markup=kb.admin('uz'))
        return state.admin
    supplier = Supplier.objects.get(id=supplier_id)
    context.bot.send_message(chat_id=supplier.chat_id, text='Sizga yangi buyurtma biriktirildi!!!')
    order = Order.objects.get(id=context.user_data['order_id'])
    order.supplier = supplier
    order.status = 'in_progress'
    order.save()
    query.delete_message()
    context.bot.send_message(chat_id=update.effective_chat.id, text='Buyurtma muvaffaqiyatli biriktirildi',
                             reply_markup=kb.admin('uz'))
    return state.admin


def get_finished_orders(update: Update, context: CallbackContext):
    """Get finished orders from database"""
    orders = Order.objects.filter(Q(status='completed') | Q(status='canceled'))
    if not orders:
        update.message.reply_text('Tugatilgan buyurtmalar mavjud emas!!!')
        return state.admin
    msg = "Tugatilgan buyurtmalar ro'yxati:\n\n"
    for order in orders[::-1][:20]:
        msg += f"{order.id}) {order.user.fullname} | {order.total_price} | {order.created_at.strftime('%d.%m.%Y %H:%M')}\n"
    update.message.reply_text(msg, reply_markup=kb.back('uz'))
    return state.admin


def get_photo(update: Update, context: CallbackContext):
    """Get photo from user"""
    update.message.reply_text("Rasmni yuboring", reply_markup=kb.back('uz'))
    return state.get_photo


def get_photo_and_send_file_id(update: Update, context: CallbackContext):
    """Get photo and send file id to user"""
    photo = update.message.photo[-1].file_id
    msg = f"Siz yuborgan rasmni fayl ID si: <code>{photo}</code>"
    update.message.reply_html(msg, reply_markup=kb.back('uz'))
    return state.get_photo