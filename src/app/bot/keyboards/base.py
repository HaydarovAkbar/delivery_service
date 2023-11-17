from app.bot.messages.main import KeyboardText as msg_text
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton


def number(number):
    """13000 -> 13 000"""
    return '{:,}'.format(number).replace(',', ' ')


def number_simvole(number):
    """13000 -> 13 000"""
    simvole = {
        '1': '1️⃣',
        '2': '2️⃣',
        '3': '3️⃣',
        '4': '4️⃣',
        '5': '5️⃣',
        '6': '6️⃣',
        '7': '7️⃣',
        '8': '8️⃣',
        '9': '9️⃣',
        '0': '0️⃣',
    }
    result = ''
    for i in str(number):
        result += simvole.get(i)
    return result


class Keyboards:
    def __init__(self):
        self._keyboards = {}

    @staticmethod
    def language():
        inline = [
            [
                InlineKeyboardButton(msg_text.languages['uz'], callback_data='uz'),
                InlineKeyboardButton(msg_text.languages['ru'], callback_data='ru'),
            ]
        ]
        return InlineKeyboardMarkup(inline)

    @staticmethod
    def phone_number(lang):
        msg = msg_text.send.get(lang)
        keyboard = [KeyboardButton(msg, request_contact=True)]
        return ReplyKeyboardMarkup([keyboard], resize_keyboard=True)

    @staticmethod
    def location(lang):
        msg = msg_text.send.get(lang)
        keyboard = [KeyboardButton(msg, request_location=True)]
        return ReplyKeyboardMarkup([keyboard], resize_keyboard=True)

    @staticmethod
    def base(lang):
        msg = msg_text.base.get(lang)
        reply_buttons = [
            [msg[0]],
            [msg[1], msg[2]],
            [msg[3], msg[4]]
        ]
        return ReplyKeyboardMarkup(reply_buttons, resize_keyboard=True)

    @staticmethod
    def back(lang):
        msg = msg_text.back.get(lang)
        reply_buttons = [
            [msg]
        ]
        return ReplyKeyboardMarkup(reply_buttons, resize_keyboard=True)

    @staticmethod
    def youtube_file_size(file_size: list):
        msg = msg_text.yt_file_types
        inline, i = [], 0
        result_size = []
        for size in file_size:
            result_size.append(str(round(size / 1024 / 1024, 2)) + ' MB')
        file_size = result_size
        for key, value in msg.items():
            inline.append([InlineKeyboardButton(value + ' - ' + file_size[i], callback_data=key)])
            i += 1
        return InlineKeyboardMarkup(inline)

    @staticmethod
    def channel(channels, lang):
        inline = []
        check = msg_text.channel.get(lang)
        for channel in channels:
            inline.append([InlineKeyboardButton(channel.title, url=channel.url)])
        inline.append([InlineKeyboardButton(check, callback_data='check_channel')])
        return InlineKeyboardMarkup(inline)

    @staticmethod
    def admin(lang):
        msg = msg_text.admin.get(lang)
        reply_buttons = [
            [msg[0], msg[1]],
            [msg[2], msg[3]],
            [msg[4], msg[5]],
            [msg[6], msg[7]],
            [msg[8], msg[9]],
            [msg[10], msg[13]],
            [msg[14]],
            [msg[15]],
            [msg[16]],
        ]
        return ReplyKeyboardMarkup(reply_buttons, resize_keyboard=True)

    @staticmethod
    def channel_set(lang):
        msg = msg_text.channel_set.get(lang)
        reply_buttons = [
            [msg[0], msg[1]],
        ]
        return ReplyKeyboardMarkup(reply_buttons, resize_keyboard=True)

    @staticmethod
    def channel_one_set(lang):
        msg = msg_text.channel_one_set.get(lang)
        reply_buttons = [
            [msg[0], msg[1]],
            [msg[2], msg[3]],
        ]
        return ReplyKeyboardMarkup(reply_buttons, resize_keyboard=True)

    @staticmethod
    def category_list(all_category):
        inline = []
        for category in all_category:
            inline.append([InlineKeyboardButton(category.name_uz, callback_data=category.id)])
        return InlineKeyboardMarkup(inline)

    @staticmethod
    def manager(lang):
        msg = msg_text.manager.get(lang)
        reply_buttons = [
            [msg[0], msg[1]],
            [msg[2]],
        ]
        return ReplyKeyboardMarkup(reply_buttons, resize_keyboard=True)

    @staticmethod
    def location_base(lang):
        msg = msg_text.get_location.get(lang)
        keyboard = ReplyKeyboardMarkup([
            [msg[0]],
            [msg[1]],
            [msg[2]],
        ], resize_keyboard=True)
        return keyboard

    @staticmethod
    def confirm(lang):
        msg = msg_text.confirmation.get(lang)
        reply_buttons = [
            [msg[0], msg[1]],
        ]
        return ReplyKeyboardMarkup(reply_buttons, resize_keyboard=True)

    @staticmethod
    def user_locations(user_locations, lang):
        msg = msg_text.back.get(lang)
        inline = []
        for location in user_locations:
            inline.append([InlineKeyboardButton(location.title, callback_data=location.id)])
        inline.append([InlineKeyboardButton(msg, callback_data='back')])
        return InlineKeyboardMarkup(inline)

    @staticmethod
    def get_category_list(categories, lang):
        msg = msg_text.product_back.get(lang)
        inline, b = [], []
        for category in categories:
            if lang == 'uz':
                b.append(InlineKeyboardButton(category.name_uz, callback_data=category.id))
            else:
                b.append(InlineKeyboardButton(category.name_ru, callback_data=category.id))
            if len(b) == 2:
                inline.append(b)
                b = []
        if b:
            inline.append(b)
        inline.append([InlineKeyboardButton(msg[3], callback_data='my_cart')])
        inline.append([InlineKeyboardButton(msg[0], callback_data='back')])
        return InlineKeyboardMarkup(inline)

    @staticmethod
    def yes_no(lang):
        msg = msg_text.yes_no.get(lang)
        reply_buttons = [
            [msg[0], msg[1]],
        ]
        return ReplyKeyboardMarkup(reply_buttons, resize_keyboard=True)

    @staticmethod
    def get_product_list(products, lang):
        msg = msg_text.product_back.get(lang)
        inline, b = [], []
        for product in products:
            if lang == 'uz':
                b.append(InlineKeyboardButton(product.name_uz, callback_data=product.id))
            else:
                b.append(InlineKeyboardButton(product.name_ru, callback_data=product.id))
            if len(b) == 2:
                inline.append(b)
                b = []
        if b:
            inline.append(b)
        inline.append([InlineKeyboardButton(msg[3], callback_data='my_cart')])
        inline.append(
            [InlineKeyboardButton(msg[0], callback_data='back')]) # InlineKeyboardButton(msg[1], callback_data='main')])
        return InlineKeyboardMarkup(inline)

    @staticmethod
    def product_size_list(product_sizes, lang):
        msg = msg_text.product_back.get(lang)
        inline, b = [], []
        for product_size in product_sizes:
            if lang == 'uz':
                b.append(InlineKeyboardButton(product_size.name_uz + ' ' + str(number(product_size.price)) + " so'm",
                                              callback_data=product_size.id))
            else:
                b.append(InlineKeyboardButton(product_size.name_ru + ' ' + str(number(product_size.price)) + " сум",
                                              callback_data=product_size.id))
            if len(b) == 2:
                inline.append(b)
                b = []
        if b:
            inline.append(b)
        inline.append([InlineKeyboardButton(msg[3], callback_data='my_cart')])
        inline.append(
            [InlineKeyboardButton(msg[0], callback_data='back')]) # InlineKeyboardButton(msg[1], callback_data='main')])
        # inline.append([InlineKeyboardButton(msg[2], callback_data='cart')])
        return InlineKeyboardMarkup(inline)
    @staticmethod
    def sell_product_count(count, lang):
        msg = msg_text.product_back.get(lang)
        minus = InlineKeyboardButton('-', callback_data='minus')
        plus = InlineKeyboardButton('+', callback_data='plus')
        count = InlineKeyboardButton(str(count), callback_data='count')
        inline = [[minus, count, plus]]
        inline.append([InlineKeyboardButton(msg[2], callback_data='cart')])
        inline.append(
            [InlineKeyboardButton(msg[0], callback_data='back')])
        return InlineKeyboardMarkup(inline)

    @staticmethod
    def cart(products, user_lang):
        msg = msg_text.cart.get(user_lang)
        inline, b = [], []
        c = 1
        for product in products:
            if user_lang == 'uz':
                b.append(InlineKeyboardButton(number_simvole(c) + ' ' + product.name_uz + ' ❌',
                                              callback_data=c - 1))
            else:
                b.append(InlineKeyboardButton(number_simvole(c) + ' ' + product.name_ru + ' ❌',
                                              callback_data=c - 1))
            if len(b) == 2:
                inline.append(b)
                b = []
            c += 1
        if b:
            inline.append(b)
        inline.append(
            [InlineKeyboardButton(msg[0], callback_data='back'), InlineKeyboardButton(msg[1], callback_data='sell')])
        inline.append(
            [InlineKeyboardButton(msg[2], callback_data='clear')])

        return InlineKeyboardMarkup(inline)

    @staticmethod
    def settings(lang):
        msg = msg_text.settings.get(lang)
        reply_buttons = [
            [msg[0], msg[1]],
            [msg[2], ]
        ]
        return ReplyKeyboardMarkup(reply_buttons, resize_keyboard=True)

    @staticmethod
    def supplier(lang):
        msg = msg_text.supplier.get(lang)
        reply_buttons = [
            [msg[0]],
            [msg[1]],
        ]
        return ReplyKeyboardMarkup(reply_buttons, resize_keyboard=True)

    @staticmethod
    def supplier_order(lang):
        msg = msg_text.supplier_order.get(lang)
        reply_buttons = [
            [msg[0], msg[1]],
            [msg[2], msg[3]],
            [msg[4], ],
        ]
        return ReplyKeyboardMarkup(reply_buttons, resize_keyboard=True)


    @staticmethod
    def supplier_list(supplier_list):
        inline = []
        for supplier in supplier_list:
            inline.append([InlineKeyboardButton(supplier.name, callback_data=supplier.id)])
        inline.append([InlineKeyboardButton("❌ o'chirish", callback_data='cencel'),
                       InlineKeyboardButton('⬅️ Orqaga', callback_data='back')])
        return InlineKeyboardMarkup(inline)


    # @staticmethod
    # def report_by_day