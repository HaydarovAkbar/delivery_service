from telegram import Update
from telegram.ext import CallbackContext
from app.bot.states import States as state
from app.bot.keyboards.base import Keyboards as kb, number as num
from app.bot.messages.main import SupplierText as msg_text
from app.models import TGUsers, Category, Products, Order, OrderItem, OrderAddress, \
    order_status, Supplier, _order_status_uz, _order_status_uz, _order_status_ru, Admin
from django.db.models import Q
import time


def supplier(update: Update, context: CallbackContext):
    admin_id = update.effective_user.id
    admin_db = Supplier.objects.filter(chat_id=admin_id)
    if admin_db:
        update.message.reply_html(msg_text.main.get('uz'), reply_markup=kb.supplier('uz'))
        return state.supplier


def unfinished_orders(update: Update, context: CallbackContext):
    user = Supplier.objects.get(chat_id=update.effective_user.id)
    orders = Order.objects.filter(supplier=user).filter(
        Q(status='new') | Q(status='delivering') | Q(status='in_progress'))
    if not orders:
        update.message.reply_html(msg_text.no_order.get('uz'), reply_markup=kb.supplier('uz'))
        return state.supplier
    msg = f"<b>🗂 Mening yakunlanmagan buyurtmalarim</b>\n\n"
    for order in orders[::-1][:3]:
        msg += f"📦 Buyurtma raqami: <code>#{order.id}</code>\n" \
               f"👤 Mijoz: <b>{order.user.fullname}</b>\n" \
               f"📲 Telefon raqami: <b>{order.user.phone_number}</b>\n" \
               f"📍 Manzili: <b>{order.location}</b>\n" \
               f"📅 Sana: <b>{order.created_at.strftime('%d.%m.%Y %H:%M')}</b>\n" \
               f"📝 Statusi: <b>{_order_status_uz.get(order.status)}</b>\n" \
               f"💰 Umumiy summa: <b>{num(order.total_price)}</b> so'm\n\n"
    msg += "...          ...          ...        ...          ...\n\n"
    msg += f"<code>📦 Buyurtmalar soni: {orders.count()}</code>"
    update.message.reply_html(msg, reply_markup=kb.supplier('uz'))
    update.message.reply_html(msg_text.one_order_code.get('uz'))
    return state.supplier_order


def supplier_order(update: Update, context: CallbackContext):
    order_id = update.message.text
    if not order_id.isdigit():
        update.message.reply_html(msg_text.error_order_id.get('uz'), reply_markup=kb.supplier('uz'))
        return state.supplier_order
    user = Supplier.objects.get(chat_id=update.effective_user.id)
    order = Order.objects.filter(supplier=user, id=order_id)
    if not order:
        update.message.reply_html(msg_text.error_order_id.get('uz'), reply_markup=kb.supplier('uz'))
        return state.supplier_order
    order = order.first()
    context.user_data['order_id'] = order.id
    msg = f"📦 Buyurtma raqami: <code>#{order.id}</code>\n" \
          f"👤 Mijoz: <b>{order.user.fullname}</b>\n" \
          f"📲 Telefon raqami: <b>{order.user.phone_number}</b>\n" \
          f"📍 Manzili: <b>{order.location}</b>\n" \
          f"📅 Sana: <b>{order.created_at.strftime('%d.%m.%Y %H:%M')}</b>\n" \
          f"📝 Statusi: <b>{_order_status_uz.get(order.status)}</b>\n" \
          f"💰 Umumiy summa: <b>{num(order.total_price)}</b> so'm\n\n"
    msg += f"    <b>🛍 Buyurtma mahsulotlari:</b>\n\n"
    for item in OrderItem.objects.filter(order=order):
        msg += f"📦 Mahsulot: <b>{item.product_size.name_uz} - {item.product.name_uz}</b>\n" \
               f"📝 Narxi: <b>{num(item.product.price)}</b> so'm\n" \
               f"📝 Soni: <b>{item.count}</b>\n" \
               f"💰 Umumiy summa: <b>{num(item.total_price)}</b> so'm\n\n"
    update.message.reply_html(msg, reply_markup=kb.supplier('uz'))
    update.message.reply_location(order.location.latitude, order.location.longitude,
                                  reply_markup=kb.supplier_order('uz'))
    return state.supplier_order_status


def supplier_order_status(update: Update, context: CallbackContext):
    order_status_ = {
        "⏳ Jaryonda": 'in_progress',
        "🏎 Yetkazyapman": 'delivering',
        "✅ Yakunlandi": 'completed',
        "❌ Qaytarildi": 'canceled'
    }
    if update.message.text in [key for key in order_status_.keys()]:
        status = order_status_.get(update.message.text)
        order_id = context.user_data['order_id']
        order = Order.objects.get(id=order_id)
        order.status = status
        order.save()
        if status == 'completed':
            context.bot.send_message(chat_id=order.user.chat_id,
                                     text=msg_text.order_completed.get('uz').format(_order_status_uz.get(status)))
            for admin in Admin.objects.filter(status=True):
                time.sleep(0.1)
                context.bot.send_message(chat_id=admin.user_id,
                                         text=msg_text.order_status_to_admins.get('uz').format(order.id,
                                                                                               order.supplier.name,
                                                                                               _order_status_uz.get(
                                                                                                   status)))
            time.sleep(0.5)
            update.message.reply_sticker(
                sticker='CAACAgIAAxkBAAEDsXth4y_D-lyD2g2ONubixWaerKccXgAC7wwAAtfG8Up7mTZAqPnSZyME')
        elif status == 'cenceled':
            context.bot.send_message(chat_id=order.user.chat_id,
                                     text=msg_text.order_completed.get(order.user.language).format(
                                         _order_status_uz.get(status)))
            for admin in Admin.objects.filter(status=True):
                time.sleep(0.1)
                context.bot.send_message(chat_id=admin.user_id,
                                         text=msg_text.order_status_to_admins.get('uz').format(order.id,
                                                                                               order.supplier.name,
                                                                                               _order_status_uz.get(
                                                                                                   status)))
            time.sleep(0.5)
            update.message.reply_sticker(
                sticker='CAACAgIAAxkBAAEKfP9lI67YTn40IGpegjDrguPj4vGDUwAC9QwAAvdriEjjbaSkNCEgRjAE')
        elif status == 'delivering':
            context.bot.send_message(chat_id=order.user.chat_id,
                                     text=msg_text.order_completed.get(order.user.language).format(
                                         _order_status_uz.get(status)))
            for admin in Admin.objects.filter(status=True):
                time.sleep(0.1)
                context.bot.send_message(chat_id=admin.user_id,
                                         text=msg_text.order_status_to_admins.get('uz').format(order.id,
                                                                                               order.supplier.name,
                                                                                               _order_status_uz.get(
                                                                                                   status)))
            time.sleep(0.5)
            update.message.reply_sticker(
                sticker='CAACAgIAAxkBAAEKfQVlI6_HT6pe9vuJbuDGeNUbhJ2nkAACMwADr8ZRGnokEoN5ub9iMAQ')
        else:
            for admin in Admin.objects.filter(status=True):
                time.sleep(0.1)
                context.bot.send_message(chat_id=admin.user_id,
                                         text=msg_text.order_status_to_admins.get('uz').format(order.id,
                                                                                               order.supplier.name,
                                                                                               _order_status_uz.get(
                                                                                                   status)))
            context.bot.send_message(chat_id=order.user.chat_id,
                                     text=msg_text.order_completed.get(order.user.language).format(
                                         _order_status_uz.get(status)))
            time.sleep(0.5)
            update.message.reply_sticker(
                sticker='CAACAgIAAxkBAAEKfQNlI68f_E2QsJLDPBD5tZbdEJ88xAACIwADKA9qFCdRJeeMIKQGMAQ')
        update.message.reply_html(msg_text.order_status.get('uz'), reply_markup=kb.supplier('uz'))
    else:
        update.message.reply_html(msg_text.error_order_status.get('uz'), reply_markup=kb.supplier('uz'))
    return state.supplier


def my_finished_orders(update: Update, context: CallbackContext):
    user = Supplier.objects.get(chat_id=update.effective_user.id)
    orders = Order.objects.filter(supplier=user, status='completed')
    if orders:
        msg = f"<b>🗂 Mening yakunlangan buyurtmalarim</b>\n\n"
        for order in orders[::-1][:3]:
            msg += f"📦 Buyurtma raqami: <code>{order.id}</code>\n" \
                   f"👤 Mijoz: <b>{order.user}</b>\n" \
                   f"📲 Telefon raqami: <b>{order.user.phone_number}</b>\n" \
                   f"📍 Manzili: <b>{order.location}</b>\n" \
                   f"📅 Sana: <b>{order.created_at.strftime('%d.%m.%Y %H:%M')}</b>\n" \
                   f"📝 Statusi: <b>{_order_status_uz.get(order.status)}</b>\n" \
                   f"💰 Umumiy summa: <b>{num(order.total_price)} so'm</b>\n\n"
        msg += "...          ...          ...        ...          ...\n\n"
        msg += f"<code>📦 Buyurtmalar soni: {orders.count()}</code>"
        update.message.reply_html(msg, reply_markup=kb.supplier('uz'))
    else:
        update.message.reply_html(msg_text.not_found_finished_order.get('uz'), reply_markup=kb.supplier('uz'))
    return state.supplier
