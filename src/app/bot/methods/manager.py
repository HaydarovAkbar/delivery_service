from datetime import datetime
from telegram import Update
from telegram.ext import CallbackContext
from app.bot.states import States as state
from app.bot.keyboards.base import Keyboards as kb, number as num
from app.bot.messages.main import MenejerText as msg_text
from app.models import Boss, TGUsers, Channel, Category, Products, Supplier, Order, OrderItem, OrderAddress, \
    order_status, Admin
from django.db.models import Q, Sum


def manager(update: Update, context: CallbackContext):
    admin_id = update.effective_user.id
    admin_db = Boss.objects.filter(user_id=admin_id)
    if admin_db:
        update.message.reply_html(msg_text.main.get('uz'), reply_markup=kb.manager('uz'))
        return state.manager


def finished_orders(update: Update, context: CallbackContext):
    orders = Order.objects.filter(status='completed')
    cencel_count = Order.objects.filter(status='canceled').count()
    delivering_count = Order.objects.filter(status='delivering').count()
    in_progress_count = Order.objects.filter(status='in_progress').count()
    new_count = Order.objects.filter(status='new').count()
    order_count = Order.objects.all().count()
    total_price = orders.aggregate(total_price_sum=Sum('total_price'))['total_price_sum']
    if not orders:
        update.message.reply_html(msg_text.not_found_finished_order.get('uz'), reply_markup=kb.manager('uz'))
        return state.manager
    msg = f"""
<b>📊 Buyurtmalar statistikasi</b>

Buyurtmalar soni status bo'yicha:

    🆕 Yangi: {new_count}
    ⏳  Jarayonda: {in_progress_count}
    🚚 Yetkazilmoqda: {delivering_count}
    ❌ Qaytarilgan: {cencel_count}
    ✅ Yakunlangan: {orders.count()}

<code>Barcha buyurtmalar soni: </code>{order_count}-ta\n
<code>Buyurtmalardan tushgan summa: </code>{num(total_price)} so'm
"""
    update.message.reply_html(msg)
    return state.manager


def subscriber_stats(update: Update, context: CallbackContext):
    user = TGUsers.objects.all()
    supplier_count = Supplier.objects.all().count()
    admin_count = Admin.objects.all().count()
    today_user = user.filter(date_of_created__date=datetime.today())
    msg = f"""
<b>📊 A'zolar statistikasi</b>
    
    🧑‍💻 Adminlar soni: {admin_count}
    🚚 Kuryerlar soni: {supplier_count}
    👤 A'zolar soni: {user.count()}

🆕 Bugun qo'shilgan a'zolar soni: {today_user.count()}
"""
    update.message.reply_html(msg)
    return state.manager


def report_by_day(update: Update, context: CallbackContext):
    orders = Order.objects.filter(created_at__date=datetime.today())
    cencel_count = orders.filter(status='canceled').count()
    delivering_count = orders.filter(status='delivering').count()
    in_progress_count = orders.filter(status='in_progress').count()
    new_count = orders.filter(status='new').count()
    complated_orders = orders.filter(status='completed')
    order_count = orders.count()
    total_price = complated_orders.aggregate(total_price_sum=Sum('total_price'))['total_price_sum']
    if not orders:
        update.message.reply_html(msg_text.not_found_finished_order.get('uz') + "\n\nQaysi kunni hisobotini ko'rmoqchisiz kiriting (Misol uchun: 2023-11-01)", reply_markup=kb.manager('uz'))
        return state.manager_report_by_day
    msg = f"""
    <b>📊 Bugungi buyurtmalar statistikasi</b>

    Buyurtmalar soni status bo'yicha:

        🆕 Yangi: {new_count}
        ⏳  Jarayonda: {in_progress_count}
        🚚 Yetkazilmoqda: {delivering_count}
        ❌ Qaytarilgan: {cencel_count}
        ✅ Yakunlangan: {complated_orders.count()}

    <code>Barcha buyurtmalar soni: </code>{order_count}-ta\n
    <code>Buyurtmalardan tushgan summa: </code>{num(total_price)} so'm
    
    
    Qaysi kunni hisoboti kerak sanani kiriting: (Misol uchun 2023-11-01)
    """
    update.message.reply_html(msg)
    return state.manager_report_by_day


def input_report_by_day(update: Update, context: CallbackContext):
    day = update.message.text  # 2021-11-01
    date = datetime.strptime(day, '%Y-%m-%d')
    orders = Order.objects.filter(created_at__date=date)
    cencel_count = orders.filter(status='canceled').count()
    delivering_count = orders.filter(status='delivering').count()
    in_progress_count = orders.filter(status='in_progress').count()
    new_count = orders.filter(status='new').count()
    complated_orders = orders.filter(status='completed')
    order_count = orders.count()
    total_price = complated_orders.aggregate(total_price_sum=Sum('total_price'))['total_price_sum']
    if not orders:
        update.message.reply_html(msg_text.not_found_finished_order.get('uz'), reply_markup=kb.manager('uz'))
        return state.manager
    msg = f"""
    <b>📊 {day} kuni buyurtmalar statistikasi</b>

    Buyurtmalar soni status bo'yicha:

        🆕 Yangi: {new_count}
        ⏳  Jarayonda: {in_progress_count}
        🚚 Yetkazilmoqda: {delivering_count}
        ❌ Qaytarilgan: {cencel_count}
        ✅ Yakunlangan: {complated_orders.count()}

    <code>Barcha buyurtmalar soni: </code>{order_count}-ta\n
    <code>Buyurtmalardan tushgan summa: </code>{num(total_price)} so'm
    """
    update.message.reply_html(msg, reply_markup=kb.manager('uz'))
    return state.manager
