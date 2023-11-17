import time

from telegram import Update, ReplyKeyboardRemove
from telegram.ext import CallbackContext
from app.bot.messages.main import MessageText as msg_text
from app.bot.keyboards.base import Keyboards as kb, number as num
from app.bot.states import States as state
from decouple import config
from datetime import datetime
from app.models import TGUsers, Caption, Channel, Admin, TgUserLocations, Category, Products, ProductSize, Order, \
    OrderItem, SupplierPrice, _order_status_uz, _order_status_ru
from django.conf import settings
from geopy.geocoders import Nominatim


def check_channel(update: Update, context: CallbackContext):
    all_channel = Channel.objects.filter(status=True)
    user_lang = TGUsers.objects.get(chat_id=update.effective_user.id).language
    left_channel = []
    for channel in all_channel:
        try:
            a = context.bot.get_chat_member(chat_id=channel.channel_id, user_id=update.effective_user.id)
            if a.status == 'left':
                left_channel.append(channel)
        except Exception as e:
            print(e)
    if left_channel:
        context.bot.send_message(chat_id=update.effective_user.id, text=msg_text.add_to_channel.get(user_lang),
                                 reply_markup=kb.channel(left_channel, user_lang))
        return state.check_channel


def add_to_channel(update: Update, context: CallbackContext):
    query = update.callback_query
    user_lang = TGUsers.objects.get(chat_id=update.effective_user.id).language
    channel = Channel.objects.filter(status=True)
    left_channel = []
    for ch in channel:
        try:
            a = context.bot.get_chat_member(chat_id=ch.channel_id, user_id=update.effective_user.id)
            if a.status == 'left':
                left_channel.append(ch)
        except Exception as e:
            print(e)

    query.delete_message()
    time.sleep(0.1)
    if left_channel:
        context.bot.send_message(chat_id=update.effective_user.id, text=msg_text.add_to_channel.get(user_lang),
                                 reply_markup=kb.channel(left_channel, user_lang))
        return state.check_channel
    return start(update, context)


def start(update: Update, context: CallbackContext):
    all_channel = Channel.objects.filter(status=True)
    user_lang = update.effective_user.language_code if update.effective_user.language_code in ['uz', 'ru'] else 'ru'
    left_channel = []
    for channel in all_channel:
        try:
            a = context.bot.get_chat_member(chat_id=channel.channel_id, user_id=update.effective_user.id)
            if a.status == 'left':
                left_channel.append(channel)
        except Exception as e:
            print(e)
    if left_channel:
        context.bot.send_message(chat_id=update.effective_user.id, text=msg_text.add_to_channel.get(user_lang),
                                 reply_markup=kb.channel(left_channel, user_lang))
        return state.check_channel
    user, _ = TGUsers.objects.get_or_create(chat_id=update.effective_user.id)
    if not _:
        if not user.language or not user.phone_number:
            context.bot.send_message(chat_id=update.effective_user.id, text=msg_text.main.get(user_lang),
                                     parse_mode='HTML',
                                     reply_markup=kb.language())
            return state.language
        user_lang = user.language
        context.bot.send_message(chat_id=update.effective_user.id, text=msg_text.base.get(user_lang), parse_mode='HTML',
                                 reply_markup=kb.base(user_lang))
        return state.main
    context.bot.send_message(chat_id=update.effective_user.id, text=msg_text.main.get(user_lang), parse_mode='HTML',
                             reply_markup=kb.language())
    return state.language


def language(update: Update, context: CallbackContext):
    all_channel = Channel.objects.filter(status=True)
    user_lang = TGUsers.objects.get(chat_id=update.effective_user.id).language
    left_channel = []
    for channel in all_channel:
        try:
            a = context.bot.get_chat_member(chat_id=channel.channel_id, user_id=update.effective_user.id)
            if a.status == 'left':
                left_channel.append(channel)
        except Exception as e:
            print(e)
    if left_channel:
        context.bot.send_message(chat_id=update.effective_user.id, text=msg_text.add_to_channel.get(user_lang),
                                 reply_markup=kb.channel(left_channel, user_lang))
        return state.check_channel
    query = update.callback_query
    user_lang = query.data
    context.user_data['lang'] = user_lang
    user = TGUsers.objects.get(chat_id=query.message.chat_id)
    user.language = user_lang
    user.username = update.effective_user.username
    user.fullname = update.effective_user.full_name[:50]
    user.save()
    query.delete_message(timeout=1)
    context.bot.send_message(chat_id=query.message.chat_id, text=msg_text.phone_number.get(user_lang),
                             reply_markup=kb.phone_number(user_lang), parse_mode='HTML')
    return state.contact


def get_contact(update: Update, context: CallbackContext):
    all_channel = Channel.objects.filter(status=True)
    user_lang = TGUsers.objects.get(chat_id=update.effective_user.id).language
    left_channel = []
    for channel in all_channel:
        try:
            a = context.bot.get_chat_member(chat_id=channel.channel_id, user_id=update.effective_user.id)
            if a.status == 'left':
                left_channel.append(channel)
        except Exception as e:
            print(e)
    if left_channel:
        context.bot.send_message(chat_id=update.effective_user.id, text=msg_text.add_to_channel.get(user_lang),
                                 reply_markup=kb.channel(left_channel, user_lang))
        return state.check_channel
    user = TGUsers.objects.get(chat_id=update.effective_user.id)
    user.phone_number = update.message.contact.phone_number
    user.save()
    update.message.reply_html(msg_text.main.get(user_lang), reply_markup=kb.base(user_lang))
    return state.main


def get_contact_text(update: Update, context: CallbackContext):
    user_msg = update.message.text
    user_db = TGUsers.objects.filter(chat_id=update.effective_user.id)
    user_lang = user_db.language
    if user_msg.startswith('+998') and len(user_msg) == 13:
        user_msg = user_msg
    elif user_msg.startswith('998') and len(user_msg) == 12:
        user_msg = '+' + user_msg
    else:
        update.message.reply_html(msg_text.phone_number_error.get(user_lang), reply_markup=kb.phone_number(user_lang))
    user_db.phone_number = user_msg
    user_db.save()
    update.message.reply_html(msg_text.main.get(user_lang), reply_markup=kb.base(user_lang))
    return state.main


def get_stats(update: Update, context: CallbackContext):
    all_channel = Channel.objects.filter(status=True)
    user_lang = TGUsers.objects.get(chat_id=update.effective_user.id).language
    left_channel = []
    for channel in all_channel:
        try:
            a = context.bot.get_chat_member(chat_id=channel.channel_id, user_id=update.effective_user.id)
            if a.status == 'left':
                left_channel.append(channel)
        except Exception as e:
            print(e)
    if left_channel:
        context.bot.send_message(chat_id=update.effective_user.id, text=msg_text.add_to_channel.get(user_lang),
                                 reply_markup=kb.channel(left_channel, user_lang))
        return state.check_channel
    user_lang = TGUsers.objects.get(chat_id=update.effective_user.id).language
    update.message.reply_html(msg_text.get_stats.get(user_lang), reply_markup=kb.back(user_lang))
    return state.get_stats


def feedback(update: Update, context: CallbackContext):
    all_channel = Channel.objects.filter(status=True)
    user_lang = TGUsers.objects.get(chat_id=update.effective_user.id).language
    left_channel = []
    for channel in all_channel:
        try:
            a = context.bot.get_chat_member(chat_id=channel.channel_id, user_id=update.effective_user.id)
            if a.status == 'left':
                left_channel.append(channel)
        except Exception as e:
            print(e)
    if left_channel:
        context.bot.send_message(chat_id=update.effective_user.id, text=msg_text.add_to_channel.get(user_lang),
                                 reply_markup=kb.channel(left_channel, user_lang))
        return state.check_channel
    user_lang = TGUsers.objects.get(chat_id=update.effective_user.id).language
    update.message.reply_html(msg_text.get_feedback.get(user_lang), reply_markup=kb.back(user_lang))
    return state.feedback


def send_feedback(update: Update, context: CallbackContext):
    group_chat_id = config('FEEDBACK_GROUP_ID')
    username = settings.USERNAME
    fullname = update.message.from_user.full_name
    user_id = update.message.from_user.id
    date = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
    user_lang = TGUsers.objects.get(chat_id=update.effective_user.id).language
    group_msg = f"""<b>
BOT: {username}

Yuboruvchi: <i>{fullname}</i>
Username: @{update.message.from_user.username}
Tg-id: <code>{user_id} </code>
Vaqti: <code>{date}</code> </b>
"""
    update.message.copy(chat_id=group_chat_id)
    time.sleep(0.1)
    context.bot.send_message(chat_id=group_chat_id, text=group_msg, parse_mode='HTML')
    update.message.reply_html(msg_text.feedback_sent.get(user_lang), reply_markup=kb.back(user_lang))
    return state.feedback


def echo(update: Update, context):
    update.message.reply_text(update.message.text)


def back(update: Update, context: CallbackContext):
    all_channel = Channel.objects.filter(status=True)
    try:
        user_lang = TGUsers.objects.get(chat_id=update.effective_user.id).language
    except Exception:
        return start(update, context)
    left_channel = []
    for channel in all_channel:
        try:
            a = context.bot.get_chat_member(chat_id=channel.channel_id, user_id=update.effective_user.id)
            if a.status == 'left':
                left_channel.append(channel)
        except Exception as e:
            print(e)
    if left_channel:
        context.bot.send_message(chat_id=update.effective_user.id, text=msg_text.add_to_channel.get(user_lang),
                                 reply_markup=kb.channel(left_channel, user_lang))
        return state.check_channel
    user_lang = TGUsers.objects.get(chat_id=update.effective_user.id).language
    update.message.reply_html(msg_text.main.get(user_lang), reply_markup=kb.base(user_lang))
    return state.main


def help(update: Update, context: CallbackContext):
    user_lang = TGUsers.objects.get(chat_id=update.effective_user.id).language
    bot_username = settings.USERNAME
    update.message.reply_html(msg_text.help.get(user_lang).replace('@Gozilla_bot', bot_username))
    return state.main


def get_location(update: Update, context: CallbackContext):
    user_lang = TGUsers.objects.get(chat_id=update.effective_user.id).language
    update.message.reply_html(msg_text.get_location.get(user_lang), reply_markup=kb.location_base(user_lang))
    return state.location


def user_locations(update: Update, context: CallbackContext):
    user_db = TGUsers.objects.get(chat_id=update.effective_user.id)
    user_lang = user_db.language
    user_locations = TgUserLocations.objects.filter(user=user_db)
    if not user_locations:
        update.message.reply_html(msg_text.not_found_location.get(user_lang), reply_markup=kb.location_base(user_lang))
        return state.location
    update.message.reply_html(msg_text.choose_location.get(user_lang),
                              reply_markup=kb.user_locations(user_locations, user_lang))
    return state.choose_location


def choose_location(update: Update, context: CallbackContext):
    query = update.callback_query
    if query.data == 'back':
        query.delete_message()
        user_lang = TGUsers.objects.get(chat_id=update.effective_user.id).language
        context.bot.send_message(chat_id=update.effective_user.id, text=msg_text.get_location.get(user_lang),
                                 parse_mode="HTML", reply_markup=kb.location_base(user_lang))
        return state.location
    user_lang = TGUsers.objects.get(chat_id=update.effective_user.id).language
    context.user_data['choose_location'] = query.data
    query.delete_message()
    context.bot.send_message(chat_id=update.effective_user.id, text=msg_text.adress_has_been_found.get(user_lang),
                             parse_mode="HTML", reply_markup=ReplyKeyboardRemove())
    category = Category.objects.all()
    context.bot.send_message(chat_id=update.effective_user.id, text=msg_text.choose_menu.get(user_lang),
                             reply_markup=kb.get_category_list(category, user_lang))
    return state.choose_category


def get_user_only_location(update: Update, context: CallbackContext):
    user_db = TGUsers.objects.get(chat_id=update.effective_user.id)
    user_lang = user_db.language
    update.message.reply_html(msg_text.get_only_location.get(user_lang), reply_markup=kb.location(user_lang))
    return state.location


def get_user_location(update: Update, context: CallbackContext):
    user_db = TGUsers.objects.get(chat_id=update.effective_user.id)
    user_lang = user_db.language
    location = update.message.location
    context.user_data['location'] = location
    update.message.reply_html(msg_text.confirmation.get(user_lang), reply_markup=kb.confirm(user_lang))
    return state.confirm_location


def confirm_location(update: Update, context: CallbackContext):
    user_db = TGUsers.objects.get(chat_id=update.effective_user.id)
    user_lang = user_db.language
    location = context.user_data['location']
    geolocator = Nominatim(
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36")
    location = geolocator.reverse((location.latitude, location.longitude))
    address = location.address
    a = TgUserLocations.objects.create(user=user_db, longitude=location.longitude, latitude=location.latitude,
                                       title=address)
    update.message.reply_html(msg_text.adress_has_been_found.get(user_lang), reply_markup=kb.back('uz'))
    category = Category.objects.all()
    context.user_data['choose_location'] = a.id
    update.message.reply_html(msg_text.choose_menu.get(user_lang),
                              reply_markup=kb.get_category_list(category, user_lang))
    return state.choose_category


def choose_category(update: Update, context: CallbackContext):
    user_lang = TGUsers.objects.get(chat_id=update.effective_user.id).language
    query = update.callback_query
    if query.data == 'back':
        query.delete_message()
        context.bot.send_message(chat_id=update.effective_user.id, text=msg_text.get_location.get(user_lang),
                                 parse_mode="HTML", reply_markup=kb.location_base(user_lang))
        return state.location
    elif query.data == 'my_cart':
        query.delete_message()
        if context.user_data.get('cart', False):
            cart = context.user_data.get('cart', False)
            cart_items, products = [], []
            c, total_price = 1, 0
            for item in cart:
                product = Products.objects.get(id=item['product'])
                products.append(product)
                product_size = ProductSize.objects.get(id=item['product_size'])
                if user_lang == 'uz':
                    cart_items.append(
                        f"{c}) {product.name_uz} │ {product_size.name_uz} │ {num(product_size.price)} so'm │ {item['count']} - ta")
                else:
                    cart_items.append(
                        f"{c}) {product.name_ru} │ {product_size.name_ru} │ {num(product_size.price)} сум │ {item['count']} - шт")
                c += 1
                total_price += product_size.price * item['count']
            if user_lang == 'uz':
                cart_items.append(f"\n♻️ Jami: {num(total_price)} so'm")
                cart_items.append(f"💸 Yetkazib berish: {num(SupplierPrice.objects.all()[0].price)} so'm")
                cart_items.append(f"💰 Umumiy: {num(total_price + SupplierPrice.objects.all()[0].price)} so'm")
            else:
                cart_items.append(f"\n♻️ Итого: {num(total_price)} сум")
                cart_items.append(f"💸 Доставка: {num(SupplierPrice.objects.all()[0].price)} сум")
                cart_items.append(f"💰 Всего: {num(total_price + SupplierPrice.objects.all()[0].price)} сум")
            context.bot.send_message(chat_id=update.effective_user.id, text='\n'.join(cart_items),
                                     reply_markup=kb.cart(products, user_lang))
            return state.index_cart
        else:
            context.bot.send_message(chat_id=update.effective_user.id, text=msg_text.cart_empty.get(user_lang),
                                     reply_markup=kb.cart([], user_lang))
            return state.index_cart
    context.user_data['category'] = query.data
    category = Category.objects.get(id=query.data)
    products = Products.objects.filter(category=query.data, status=True)
    query.delete_message()
    photo = category.image_uz if user_lang == 'uz' else category.image_ru
    context.bot.send_photo(chat_id=update.effective_user.id, photo=photo, caption=msg_text.choose_menu.get(user_lang),
                           reply_markup=kb.get_product_list(products, user_lang))
    return state.choose_product


def choose_product(update: Update, context: CallbackContext):
    query = update.callback_query
    user_lang = TGUsers.objects.get(chat_id=update.effective_user.id).language
    if query.data == 'back':
        query.delete_message()
        category = Category.objects.all()
        context.bot.send_message(chat_id=update.effective_user.id, text=msg_text.choose_menu.get(user_lang),
                                 reply_markup=kb.get_category_list(category, user_lang))
        return state.choose_category
    elif query.data == 'main':
        query.delete_message()
        context.bot.send_message(chat_id=update.effective_user.id, text=msg_text.base.get(user_lang), parse_mode="HTML",
                                 reply_markup=kb.base(user_lang))
        return state.main
    elif query.data == 'my_cart':
        query.delete_message()
        if context.user_data.get('cart', False):
            cart = context.user_data.get('cart', False)
            cart_items, products = [], []
            c, total_price = 1, 0
            for item in cart:
                product = Products.objects.get(id=item['product'])
                products.append(product)
                product_size = ProductSize.objects.get(id=item['product_size'])
                if user_lang == 'uz':
                    cart_items.append(
                        f"{c}) {product.name_uz} │ {product_size.name_uz} │ {num(product_size.price)} so'm │ {item['count']} - ta")
                else:
                    cart_items.append(
                        f"{c}) {product.name_ru} │ {product_size.name_ru} │ {num(product_size.price)} сум │ {item['count']} - шт")
                c += 1
                total_price += product_size.price * item['count']
            if user_lang == 'uz':
                cart_items.append(f"\n♻️ Jami: {num(total_price)} so'm")
                cart_items.append(f"💸 Yetkazib berish: {num(SupplierPrice.objects.all()[0].price)} so'm")
                cart_items.append(f"💰 Umumiy: {num(total_price + SupplierPrice.objects.all()[0].price)} so'm")
            else:
                cart_items.append(f"\n♻️ Итого: {num(total_price)} сум")
                cart_items.append(f"💸 Доставка: {num(SupplierPrice.objects.all()[0].price)} сум")
                cart_items.append(f"💰 Всего: {num(total_price + SupplierPrice.objects.all()[0].price)} сум")
            context.bot.send_message(chat_id=update.effective_user.id, text='\n'.join(cart_items),
                                     reply_markup=kb.cart(products, user_lang))
            return state.index_cart
        else:
            context.bot.send_message(chat_id=update.effective_user.id, text=msg_text.cart_empty.get(user_lang),
                                     reply_markup=kb.cart([], user_lang))
            return state.index_cart
    context.user_data['product'] = query.data
    product = Products.objects.get(id=query.data)
    product_sizes = ProductSize.objects.filter(product=query.data)
    query.delete_message()
    if user_lang == 'uz':
        context.bot.send_photo(chat_id=update.effective_user.id, photo=product.image,
                               caption=msg_text.choose_menu.get(
                                   user_lang) + '\n\n' + product.name_uz + '\n' + product.content_uz,
                               reply_markup=kb.product_size_list(product_sizes, user_lang))
    else:
        context.bot.send_photo(chat_id=update.effective_user.id, photo=product.image,
                               caption=msg_text.choose_menu.get(
                                   user_lang) + '\n' + product.name_ru + '\n' + product.content_ru,
                               reply_markup=kb.product_size_list(product_sizes, user_lang))
    return state.choose_product_size



def choose_product_size(update: Update, context: CallbackContext):
    query = update.callback_query
    user_lang = TGUsers.objects.get(chat_id=update.effective_user.id).language
    if query.data == 'back':
        query.delete_message()
        category = Category.objects.get(id=context.user_data['category'])
        products = Products.objects.filter(category=context.user_data['category'], status=True)
        context.bot.send_photo(chat_id=update.effective_user.id, photo=category.image_uz,
                               caption=msg_text.choose_menu.get(user_lang),
                               reply_markup=kb.get_product_list(products, user_lang))
        return state.choose_product
    elif query.data == 'main':
        query.delete_message()
        context.bot.send_message(chat_id=update.effective_user.id, text=msg_text.base.get(user_lang), parse_mode="HTML",
                                 reply_markup=kb.base(user_lang))
        return state.main
    elif query.data == 'cart':
        query.delete_message()
        context.bot.send_message(chat_id=update.effective_user.id, text=msg_text.base.get(user_lang), parse_mode="HTML",
                                 reply_markup=kb.base(user_lang))
        return state.main
    elif query.data == 'my_cart':
        query.delete_message()
        if context.user_data.get('cart', False):
            cart = context.user_data.get('cart', False)
            cart_items, products = [], []
            c, total_price = 1, 0
            for item in cart:
                product = Products.objects.get(id=item['product'])
                products.append(product)
                product_size = ProductSize.objects.get(id=item['product_size'])
                if user_lang == 'uz':
                    cart_items.append(
                        f"{c}) {product.name_uz} │ {product_size.name_uz} │ {num(product_size.price)} so'm │ {item['count']} - ta")
                else:
                    cart_items.append(
                        f"{c}) {product.name_ru} │ {product_size.name_ru} │ {num(product_size.price)} сум │ {item['count']} - шт")
                c += 1
                total_price += product_size.price * item['count']
            if user_lang == 'uz':
                cart_items.append(f"\n♻️ Jami: {num(total_price)} so'm")
                cart_items.append(f"💸 Yetkazib berish: {num(SupplierPrice.objects.all()[0].price)} so'm")
                cart_items.append(f"💰 Umumiy: {num(total_price + SupplierPrice.objects.all()[0].price)} so'm")
            else:
                cart_items.append(f"\n♻️ Итого: {num(total_price)} сум")
                cart_items.append(f"💸 Доставка: {num(SupplierPrice.objects.all()[0].price)} сум")
                cart_items.append(f"💰 Всего: {num(total_price + SupplierPrice.objects.all()[0].price)} сум")
            context.bot.send_message(chat_id=update.effective_user.id, text='\n'.join(cart_items),
                                     reply_markup=kb.cart(products, user_lang))
            return state.index_cart
        else:
            context.bot.send_message(chat_id=update.effective_user.id, text=msg_text.cart_empty.get(user_lang),
                                     reply_markup=kb.cart([], user_lang))
            return state.index_cart
    context.user_data['product_size'] = query.data
    context.user_data['count'] = 1
    query.edit_message_reply_markup(
        reply_markup=kb.sell_product_count(1, user_lang))
    return state.sell_product_count


def index_cart(update: Update, context: CallbackContext):
    query = update.callback_query
    user_lang = TGUsers.objects.get(chat_id=update.effective_user.id).language
    if query.data == 'back':
        query.delete_message()
        category = Category.objects.all()
        context.bot.send_message(chat_id=update.effective_user.id, text=msg_text.choose_menu.get(user_lang),
                                 reply_markup=kb.get_category_list(category, user_lang))
        return state.choose_category
    elif query.data == 'sell':
        # Order create
        query.delete_message()
        cart = context.user_data.get('cart', [])
        if not cart:
            context.bot.send_message(chat_id=update.effective_user.id, text=msg_text.cart_empty.get(user_lang),
                                     reply_markup=kb.cart([], user_lang))
            return state.my_cart
        delivery_price = SupplierPrice.objects.all()[0].price
        total_price = 0
        for item in cart:
            product_size = ProductSize.objects.get(id=item['product_size'])
            price = product_size.price * item['count']
            total_price += price
        total_price += delivery_price
        order = Order.objects.create(
            user=TGUsers.objects.get(chat_id=update.effective_user.id),
            total_price=total_price,
            delivery_price=delivery_price,
            status='new',
            location=TgUserLocations.objects.get(id=cart[0]['location']),
        )
        for item in cart:
            product_size = ProductSize.objects.get(id=item['product_size'])
            price = product_size.price * item['count']
            OrderItem.objects.create(
                order=order,
                product_size=product_size,
                product=Products.objects.get(id=item['product']),
                count=item['count'],
                total_price=price,
            )
        notification_admins(update, context)
        context.user_data['cart'] = []
        context.bot.send_message(chat_id=update.effective_user.id, text=msg_text.order_created.get(user_lang),
                                 parse_mode="HTML",
                                 reply_markup=kb.base(user_lang))
        return state.main
    elif query.data == 'clear':
        # Clear cart
        query.delete_message()
        context.user_data['cart'] = []
        context.bot.send_message(chat_id=update.effective_user.id, text=msg_text.cart_empty.get(user_lang),
                                 reply_markup=kb.cart([], user_lang))
        return state.index_cart
    else:
        # Delete item from cart
        cart = context.user_data.get('cart', False)
        cart.pop(int(query.data))
        context.user_data['cart'] = cart
        query.delete_message()
        if cart:
            cart_items, products = [], []
            c, total_price = 1, 0
            for item in cart:
                product = Products.objects.get(id=item['product'])
                products.append(product)
                product_size = ProductSize.objects.get(id=item['product_size'])
                if user_lang == 'uz':
                    cart_items.append(
                        f"{c}) {product.name_uz} │ {product_size.name_uz} │ {num(product_size.price)} so'm │ {item['count']} - ta")
                else:
                    cart_items.append(
                        f"{c}) {product.name_ru} │ {product_size.name_ru} │ {num(product_size.price)} сум │ {item['count']} - шт")
                c += 1
                total_price += product_size.price * item['count']
            if user_lang == 'uz':
                cart_items.append(f"\n♻️ Jami: {num(total_price)} so'm")
                cart_items.append(f"💸 Yetkazib berish: {num(SupplierPrice.objects.all()[0].price)} so'm")
                cart_items.append(f"💰 Umumiy: {num(total_price + SupplierPrice.objects.all()[0].price)} so'm")
            else:
                cart_items.append(f"\n♻️ Итого: {num(total_price)} сум")
                cart_items.append(f"💸 Доставка: {num(SupplierPrice.objects.all()[0].price)} сум")
                cart_items.append(f"💰 Всего: {num(total_price + SupplierPrice.objects.all()[0].price)} сум")
            context.bot.send_message(chat_id=update.effective_user.id, text='\n'.join(cart_items),
                                     reply_markup=kb.cart(products, user_lang))
        else:
            context.bot.send_message(chat_id=update.effective_user.id, text=msg_text.cart_empty.get(user_lang),
                                     reply_markup=kb.cart([], user_lang))
        return state.index_cart


def sell_product_count(update: Update, context: CallbackContext):
    query = update.callback_query
    user_lang = TGUsers.objects.get(chat_id=update.effective_user.id).language
    if query.data == 'back':
        query.delete_message()
        product_sizes = ProductSize.objects.filter(product=context.user_data['product'])
        context.bot.send_photo(chat_id=update.effective_user.id, photo=product_sizes[0].product.image,
                               caption=msg_text.choose_menu.get(user_lang),
                               reply_markup=kb.product_size_list(product_sizes, user_lang))
        return state.choose_product_size
    elif query.data == 'main':
        query.delete_message()
        context.bot.send_message(chat_id=update.effective_user.id, text=msg_text.base.get(user_lang), parse_mode="HTML",
                                 reply_markup=kb.base(user_lang))
        return state.main
    elif query.data == 'cart':
        # query.delete_message()
        cart_item = {
            'product': context.user_data['product'],
            'product_size': context.user_data['product_size'],
            'count': context.user_data['count'],
            'category': context.user_data['category'],
            'location': context.user_data['choose_location'],
        }
        if context.user_data.get('cart', False):
            cart = context.user_data.get('cart', False)
            cart.append(cart_item)
            context.user_data['cart'] = cart
        else:
            context.user_data['cart'] = [cart_item]
        query.answer(text=msg_text.added_to_cart.get(user_lang))
        query.delete_message()
        if user_lang == 'uz':
            photo = Category.objects.get(id=context.user_data['category']).image_uz
        else:
            photo = Category.objects.get(id=context.user_data['category']).image_ru
        products = Products.objects.filter(category=context.user_data['category'])
        context.bot.send_photo(chat_id=update.effective_user.id, photo=photo,
                               caption=msg_text.choose_menu.get(user_lang),
                               reply_markup=kb.get_product_list(products, user_lang))
        return state.choose_product
    elif query.data == 'plus':
        count = context.user_data['count']
        count += 1
        context.user_data['count'] = count
        query.answer(text=msg_text.change_code.get(user_lang).format(count))
        query.edit_message_reply_markup(
            reply_markup=kb.sell_product_count(count, user_lang))
        return state.sell_product_count
    elif query.data == 'minus':
        count = context.user_data['count']
        if count > 1:
            count -= 1
        query.answer(text=msg_text.change_code.get(user_lang).format(count))
        context.user_data['count'] = count
        query.edit_message_reply_markup(
            reply_markup=kb.sell_product_count(count, user_lang))
        return state.sell_product_count


def my_cart(update: Update, context: CallbackContext):
    update.message.reply_html('✅✅✅', reply_markup=ReplyKeyboardRemove())
    user_lang = TGUsers.objects.get(chat_id=update.effective_user.id).language
    if context.user_data.get('cart', False):
        cart = context.user_data.get('cart', False)
        cart_items, products = [], []
        c, total_price = 1, 0
        for item in cart:
            product = Products.objects.get(id=item['product'])
            products.append(product)
            product_size = ProductSize.objects.get(id=item['product_size'], status=True)
            if user_lang == 'uz':
                cart_items.append(
                    f"{c}) {product.name_uz} │ {product_size.name_uz} │ {num(product_size.price)} so'm │ {item['count']} - ta")
            else:
                cart_items.append(
                    f"{c}) {product.name_ru} │ {product_size.name_ru} │ {num(product_size.price)} сум │ {item['count']} - шт")
            c += 1
            total_price += product_size.price * item['count']
        if user_lang == 'uz':
            cart_items.append(f"\n♻️ Jami: {num(total_price)} so'm")
            cart_items.append(f"💸 Yetkazib berish: {num(SupplierPrice.objects.all()[0].price)} so'm")
            cart_items.append(f"💰 Umumiy: {num(total_price + SupplierPrice.objects.all()[0].price)} so'm")
        else:
            cart_items.append(f"\n♻️ Итого: {num(total_price)} сум")
            cart_items.append(f"💸 Доставка: {num(SupplierPrice.objects.all()[0].price)} сум")
            cart_items.append(f"💰 Всего: {num(total_price + SupplierPrice.objects.all()[0].price)} сум")
        context.bot.send_message(chat_id=update.effective_user.id, text='\n'.join(cart_items),
                                 reply_markup=kb.cart(products, user_lang))
        return state.my_cart
    else:
        context.bot.send_message(chat_id=update.effective_user.id, text=msg_text.cart_empty.get(user_lang),
                                 reply_markup=kb.cart([], user_lang))
        return state.my_cart


def notification_admins(update: Update, context: CallbackContext):
    admins = Admin.objects.all()

    for admin in admins:
        context.bot.send_message(chat_id=admin.user_id, text=msg_text.notification_admins.get('uz'), parse_mode="HTML")


def cart(update: Update, context: CallbackContext):
    query = update.callback_query
    user_lang = TGUsers.objects.get(chat_id=update.effective_user.id).language
    if query.data == 'back':
        query.delete_message()
        context.bot.send_message(chat_id=update.effective_user.id, text=msg_text.base.get(user_lang), parse_mode="HTML",
                                 reply_markup=kb.base(user_lang))
        return state.main
    elif query.data == 'sell':
        # Order create
        query.delete_message()
        cart = context.user_data.get('cart', [])
        if not cart:
            context.bot.send_message(chat_id=update.effective_user.id, text=msg_text.cart_empty.get(user_lang),
                                     reply_markup=kb.cart([], user_lang))
            return state.my_cart
        delivery_price = SupplierPrice.objects.all()[0].price
        total_price = 0
        for item in cart:
            product_size = ProductSize.objects.get(id=item['product_size'])
            price = product_size.price * item['count']
            total_price += price
        total_price += delivery_price
        order = Order.objects.create(
            user=TGUsers.objects.get(chat_id=update.effective_user.id),
            total_price=total_price,
            delivery_price=delivery_price,
            status='new',
            location=TgUserLocations.objects.get(id=cart[0]['location']),
        )
        for item in cart:
            product_size = ProductSize.objects.get(id=item['product_size'])
            price = product_size.price * item['count']
            OrderItem.objects.create(
                order=order,
                product_size=product_size,
                product=Products.objects.get(id=item['product']),
                count=item['count'],
                total_price=price,
            )
        notification_admins(update, context)
        context.user_data['cart'] = []
        context.bot.send_message(chat_id=update.effective_user.id, text=msg_text.order_created.get(user_lang),
                                 parse_mode="HTML",
                                 reply_markup=kb.base(user_lang))
        return state.main
    elif query.data == 'clear':
        # Clear cart
        query.delete_message()
        context.user_data['cart'] = []
        context.bot.send_message(chat_id=update.effective_user.id, text=msg_text.cart_empty.get(user_lang),
                                 reply_markup=kb.cart([], user_lang))
        return state.my_cart
    else:
        # Delete item from cart
        cart = context.user_data.get('cart', False)
        cart.pop(int(query.data))
        context.user_data['cart'] = cart
        query.delete_message()
        if cart:
            cart_items, products = [], []
            c, total_price = 1, 0
            for item in cart:
                product = Products.objects.get(id=item['product'])
                products.append(product)
                product_size = ProductSize.objects.get(id=item['product_size'])
                if user_lang == 'uz':
                    cart_items.append(
                        f"{c}) {product.name_uz} │ {product_size.name_uz} │ {num(product_size.price)} so'm │ {item['count']} - ta")
                else:
                    cart_items.append(
                        f"{c}) {product.name_ru} │ {product_size.name_ru} │ {num(product_size.price)} сум │ {item['count']} - шт")
                c += 1
                total_price += product_size.price * item['count']
            if user_lang == 'uz':
                cart_items.append(f"\n♻️ Jami: {num(total_price)} so'm")
                cart_items.append(f"💸 Yetkazib berish: {num(SupplierPrice.objects.all()[0].price)} so'm")
                cart_items.append(f"💰 Umumiy: {num(total_price + SupplierPrice.objects.all()[0].price)} so'm")
            else:
                cart_items.append(f"\n♻️ Итого: {num(total_price)} сум")
                cart_items.append(f"💸 Доставка: {num(SupplierPrice.objects.all()[0].price)} сум")
                cart_items.append(f"💰 Всего: {num(total_price + SupplierPrice.objects.all()[0].price)} сум")
            context.bot.send_message(chat_id=update.effective_user.id, text='\n'.join(cart_items),
                                     reply_markup=kb.cart(products, user_lang))
        else:
            context.bot.send_message(chat_id=update.effective_user.id, text=msg_text.cart_empty.get(user_lang),
                                     reply_markup=kb.cart([], user_lang))
        return state.my_cart


def get_order_list(update: Update, context: CallbackContext):
    user_lang = TGUsers.objects.get(chat_id=update.effective_user.id).language
    orders = Order.objects.filter(user=TGUsers.objects.get(chat_id=update.effective_user.id))
    if orders:
        order_list = []
        if user_lang == 'uz':
            order_list.append(
                f"<code>ID │ Jami summa │ Vaqti │ 🔹 Xolati\n</code>")
        else:
            order_list.append(
                f"<code>ID │ Общая сумма │ Время │ 🔹 Статус\n</code>")
        for order in orders:
            if user_lang == 'uz':
                order_list.append(
                    f"{order.id} │ {num(order.total_price)} so'm │ {order.created_at.strftime('%d-%m-%Y %H:%M')} │ 🔹 {_order_status_uz.get(order.status)}")
            else:
                order_list.append(
                    f"{order.id} │ {num(order.total_price)} сум │ {order.created_at.strftime('%d-%m-%Y %H:%M')} │ 🔹 {_order_status_ru.get(order.status)}")
        msg = msg_text.order_history.get(user_lang) + '\n\n' + '\n'.join(order_list)
        update.message.reply_html(msg,
                                  reply_markup=kb.back(user_lang))
        return state.main
    else:
        update.message.reply_html(msg_text.order_not_found.get(user_lang), reply_markup=kb.base(user_lang))
        return state.main


def mysettings(update: Update, context: CallbackContext):
    user_lang = TGUsers.objects.get(chat_id=update.effective_user.id).language
    update.message.reply_html(msg_text.settings.get(user_lang), reply_markup=kb.settings(user_lang))
    return state.settings


def change_language_settings(update: Update, context: CallbackContext):
    user_lang = TGUsers.objects.get(chat_id=update.effective_user.id).language
    update.message.reply_html(msg_text.change_language.get(user_lang), reply_markup=kb.language())
    return state.change_language


def change_language_settings_text(update: Update, context: CallbackContext):
    user_lang = TGUsers.objects.get(chat_id=update.effective_user.id)
    query = update.callback_query
    user_lang.language = query.data
    user_lang.save()
    query.delete_message()
    context.bot.send_message(chat_id=update.effective_user.id,
                             text=msg_text.successfuly_changed_language.get(user_lang.language),
                             parse_mode="HTML",
                             reply_markup=kb.settings(user_lang.language))
    return state.settings


def change_phone_number(update: Update, context: CallbackContext):
    user_lang = TGUsers.objects.get(chat_id=update.effective_user.id).language
    update.message.reply_html(msg_text.change_phone_number.get(user_lang), reply_markup=kb.phone_number(user_lang))
    return state.change_phone_number


def change_phone_number_text(update: Update, context: CallbackContext):
    user = TGUsers.objects.get(chat_id=update.effective_user.id)
    if update.message.contact:
        user.phone_number = update.message.contact.phone_number
        user.save()
        update.message.reply_html(msg_text.successfuly_changed_phone_number.get(user.language),
                                  reply_markup=kb.settings(user.language))
        return state.settings
    else:
        user_msg = update.message.text
        if user_msg.startswith('+998') and len(user_msg) == 13:
            user_msg = user_msg
        elif user_msg.startswith('998') and len(user_msg) == 12:
            user_msg = '+' + user_msg
        else:
            update.message.reply_html(msg_text.phone_number_error.get(user.language),
                                      reply_markup=kb.phone_number(user.language))
            return state.change_phone_number
        user.phone_number = user_msg
        user.save()
        update.message.reply_html(msg_text.successfuly_changed_phone_number.get(user.language),
                                  reply_markup=kb.settings(user.language))
        return state.settings
