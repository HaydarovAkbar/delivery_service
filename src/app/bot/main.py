from telegram import Update, Bot
from telegram.ext import Dispatcher, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackContext, \
    CallbackQueryHandler
from decouple import config
from django.conf import settings
from .methods.base import start, language, feedback, send_feedback, mysettings, back, \
    help, add_to_channel, get_location, get_contact_text, get_contact, user_locations, get_user_only_location, \
    confirm_location, get_user_location, choose_location, choose_category, choose_product, choose_product_size, \
    sell_product_count, my_cart, cart, get_order_list, change_language_settings, change_language_settings_text, \
    change_phone_number, change_phone_number_text, index_cart
from .methods.admin import admin, search_user, bot_users, channel, all_admin, admin_back, channel_add, \
    channel_add_title, channel_add_url, channel_add_id, channel_one_set, admin_del, add_category, \
    get_category, all_category, category_del, add_product, get_product_name, add_product_price, get_product_content, \
    add_product_discount, add_product_photo, add_product_category, all_product, product_del, add_admin, \
    get_admin_chat_id, add_supplier, get_supplier_chat_id, get_supplier_name, get_supplier_phone, supplier_del, \
    all_supplier, adversting, get_adversting, get_unfinished_orders, get_category_image_uz, get_category_image_ru, \
    product_no_size, product_yes_size, product_size_name, product_size_price, get_order_id, choose_order_supplier, \
    get_finished_orders, get_photo, get_photo_and_send_file_id
from .methods.manager import manager, finished_orders, subscriber_stats, report_by_day, input_report_by_day
from .methods.supplier import supplier, unfinished_orders, my_finished_orders, supplier_order, supplier_order_status
import logging
from .states import States as state
from .messages.main import KeyboardText as msg_text

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


def run():
    print('started webhook')
    bot.set_webhook(settings.HOST + '/bot/')


bot: Bot = Bot(token=config('TOKEN'))

dispatcher = Dispatcher(bot, None)

all_handler = ConversationHandler(
    entry_points=[
        CommandHandler('start', start),
        CommandHandler('help', help),
        CommandHandler('admin', admin),
        CommandHandler('boss', manager),
        CommandHandler('supplier', supplier),

        MessageHandler(Filters.regex('^(' + msg_text.base['uz'][0] + ')$'), get_location),
        MessageHandler(Filters.regex('^(' + msg_text.base['uz'][1] + ')$'), my_cart),
        MessageHandler(Filters.regex('^(' + msg_text.base['uz'][2] + ')$'), get_order_list),
        MessageHandler(Filters.regex('^(' + msg_text.base['uz'][3] + ')$'), feedback),
        MessageHandler(Filters.regex('^(' + msg_text.base['uz'][4] + ')$'), mysettings),

        MessageHandler(Filters.regex('^(' + msg_text.base['ru'][0] + ')$'), get_location),
        MessageHandler(Filters.regex('^(' + msg_text.base['ru'][1] + ')$'), my_cart),
        MessageHandler(Filters.regex('^(' + msg_text.base['ru'][2] + ')$'), get_order_list),
        MessageHandler(Filters.regex('^(' + msg_text.base['ru'][3] + ')$'), feedback),
        MessageHandler(Filters.regex('^(' + msg_text.base['ru'][4] + ')$'), mysettings),

        MessageHandler(Filters.regex('^(' + msg_text.back['uz'] + ')$'), back),
        MessageHandler(Filters.regex('^(' + msg_text.back['ru'] + ')$'), back),
        MessageHandler(Filters.regex('^(' + msg_text.back['en'] + ')$'), back),
    ],
    states={
        state.language: [CommandHandler('start', start),
                         CommandHandler('help', help),
                         CommandHandler('admin', admin),
                         CommandHandler('boss', manager),
                         CommandHandler('supplier', supplier),

                         CallbackQueryHandler(language, pattern='^(uz|ru|en)$')],
        state.contact: [CommandHandler('start', start),
                        CommandHandler('help', help),
                        CommandHandler('admin', admin),
                        CommandHandler('boss', manager),
                        CommandHandler('supplier', supplier),
                        MessageHandler(Filters.contact, get_contact),
                        MessageHandler(Filters.text, get_contact_text),
                        ],
        state.main: [
            CommandHandler('start', start),
            CommandHandler('help', help),
            CommandHandler('admin', admin),
            CommandHandler('boss', manager),
            CommandHandler('supplier', supplier),

            MessageHandler(Filters.regex('^(' + msg_text.base['uz'][0] + ')$'), get_location),
            MessageHandler(Filters.regex('^(' + msg_text.base['uz'][1] + ')$'), my_cart),
            MessageHandler(Filters.regex('^(' + msg_text.base['uz'][2] + ')$'), get_order_list),
            MessageHandler(Filters.regex('^(' + msg_text.base['uz'][3] + ')$'), feedback),
            MessageHandler(Filters.regex('^(' + msg_text.base['uz'][4] + ')$'), mysettings),

            MessageHandler(Filters.regex('^(' + msg_text.base['ru'][0] + ')$'), get_location),
            MessageHandler(Filters.regex('^(' + msg_text.base['ru'][1] + ')$'), my_cart),
            MessageHandler(Filters.regex('^(' + msg_text.base['ru'][2] + ')$'), get_order_list),
            MessageHandler(Filters.regex('^(' + msg_text.base['ru'][3] + ')$'), feedback),
            MessageHandler(Filters.regex('^(' + msg_text.base['ru'][4] + ')$'), mysettings),

            MessageHandler(Filters.regex('^(' + msg_text.back['uz'] + ')$'), back),
            MessageHandler(Filters.regex('^(' + msg_text.back['ru'] + ')$'), back),
            MessageHandler(Filters.regex('^(' + msg_text.back['en'] + ')$'), back),
        ],
        state.feedback: [
            CommandHandler('start', start),
            CommandHandler('help', help),
            CommandHandler('admin', admin),
            CommandHandler('boss', manager),
            CommandHandler('supplier', supplier),

            MessageHandler(Filters.regex('^(' + msg_text.back['uz'] + ')$'), back),
            MessageHandler(Filters.regex('^(' + msg_text.back['ru'] + ')$'), back),
            MessageHandler(Filters.regex('^(' + msg_text.back['en'] + ')$'), back),
            MessageHandler(Filters.all, send_feedback)],
        state.check_channel: [
            CommandHandler('start', start),
            CommandHandler('help', help),
            CommandHandler('admin', admin),
            CommandHandler('boss', manager),
            CommandHandler('supplier', supplier),

            CallbackQueryHandler(add_to_channel), ],

        state.admin: [
            CommandHandler('start', start),
            CommandHandler('help', help),
            CommandHandler('admin', admin),
            CommandHandler('boss', manager),
            CommandHandler('supplier', supplier),

            MessageHandler(Filters.regex('^(' + msg_text.back['uz'] + ')$'), admin_back),
            MessageHandler(Filters.regex('^(' + msg_text.back['uz'] + ')$'), admin_back),
            MessageHandler(Filters.regex('^(' + msg_text.back['uz'] + ')$'), admin_back),

            MessageHandler(Filters.regex('^(' + msg_text.admin['uz'][0] + ')$'), channel_add),
            MessageHandler(Filters.regex('^(' + msg_text.admin['uz'][1] + ')$'), channel),
            MessageHandler(Filters.regex('^(' + msg_text.admin['uz'][2] + ')$'), bot_users),
            MessageHandler(Filters.regex('^(' + msg_text.admin['uz'][3] + ')$'), add_category),
            MessageHandler(Filters.regex('^(' + msg_text.admin['uz'][4] + ')$'), all_category),
            MessageHandler(Filters.regex('^(' + msg_text.admin['uz'][5] + ')$'), add_product),
            MessageHandler(Filters.regex('^(' + msg_text.admin['uz'][6] + ')$'), all_product),
            MessageHandler(Filters.regex('^(' + msg_text.admin['uz'][7] + ')$'), add_admin),
            MessageHandler(Filters.regex('^(' + msg_text.admin['uz'][8] + ')$'), all_admin),
            MessageHandler(Filters.regex('^(' + msg_text.admin['uz'][9] + ')$'), add_supplier),
            MessageHandler(Filters.regex('^(' + msg_text.admin['uz'][10] + ')$'), all_supplier),
            MessageHandler(Filters.regex('^(' + msg_text.admin['uz'][11] + ')$'), admin_back),
            MessageHandler(Filters.regex('^(' + msg_text.admin['uz'][12] + ')$'), admin_back),
            MessageHandler(Filters.regex('^(' + msg_text.admin['uz'][13] + ')$'), adversting),

            MessageHandler(Filters.regex('^(' + msg_text.admin['uz'][14] + ')$'), get_unfinished_orders),
            MessageHandler(Filters.regex('^(' + msg_text.admin['uz'][15] + ')$'), get_finished_orders),
            MessageHandler(Filters.regex('^(' + msg_text.admin['uz'][16] + ')$'), get_photo),

            MessageHandler(Filters.regex('^(' + msg_text.admin['ru'][0] + ')$'), channel_add),
            MessageHandler(Filters.regex('^(' + msg_text.admin['ru'][1] + ')$'), channel),
            MessageHandler(Filters.regex('^(' + msg_text.admin['ru'][2] + ')$'), bot_users),
            MessageHandler(Filters.regex('^(' + msg_text.admin['ru'][3] + ')$'), add_category),
            MessageHandler(Filters.regex('^(' + msg_text.admin['ru'][4] + ')$'), all_category),
            MessageHandler(Filters.regex('^(' + msg_text.admin['ru'][5] + ')$'), add_product),
            MessageHandler(Filters.regex('^(' + msg_text.admin['ru'][6] + ')$'), all_product),
            MessageHandler(Filters.regex('^(' + msg_text.admin['ru'][7] + ')$'), add_admin),
            MessageHandler(Filters.regex('^(' + msg_text.admin['ru'][8] + ')$'), all_admin),
            MessageHandler(Filters.regex('^(' + msg_text.admin['ru'][9] + ')$'), add_supplier),
            MessageHandler(Filters.regex('^(' + msg_text.admin['ru'][10] + ')$'), all_supplier),
            MessageHandler(Filters.regex('^(' + msg_text.admin['ru'][11] + ')$'), admin_back),
            MessageHandler(Filters.regex('^(' + msg_text.admin['ru'][12] + ')$'), admin_back),
            MessageHandler(Filters.regex('^(' + msg_text.admin['ru'][13] + ')$'), adversting),

            MessageHandler(Filters.regex('^(' + msg_text.admin['ru'][14] + ')$'), get_unfinished_orders),
            MessageHandler(Filters.regex('^(' + msg_text.admin['ru'][15] + ')$'), get_finished_orders),
            MessageHandler(Filters.regex('^(' + msg_text.admin['ru'][16] + ')$'), get_photo),
        ],
        state.search_user: [
            CommandHandler('start', start),
            CommandHandler('help', help),
            CommandHandler('admin', admin),
            CommandHandler('boss', manager),
            CommandHandler('supplier', supplier),

            MessageHandler(Filters.regex('^(' + msg_text.back['uz'] + ')$'), admin_back),
            MessageHandler(Filters.regex('^(' + msg_text.back['ru'] + ')$'), admin_back),
            MessageHandler(Filters.regex('^(' + msg_text.back['en'] + ')$'), admin_back),
            MessageHandler(Filters.text, search_user)
        ],

        state.channel_set: [
            CommandHandler('start', start),
            CommandHandler('help', help),
            CommandHandler('admin', admin),
            CommandHandler('supplier', supplier),

            MessageHandler(Filters.regex('^(' + msg_text.channel_set['uz'][1] + ')$'), admin_back),
            MessageHandler(Filters.text, channel_one_set)
        ],

        state.channel_add_title: [
            CommandHandler('start', start),
            CommandHandler('help', help),
            CommandHandler('admin', admin),
            CommandHandler('supplier', supplier),

            MessageHandler(Filters.regex('^(' + msg_text.channel_set['uz'][1] + ')$'), admin_back),
            MessageHandler(Filters.text, channel_add_title)
        ],
        state.channel_add_url: [
            CommandHandler('start', start),
            CommandHandler('help', help),
            CommandHandler('admin', admin),
            CommandHandler('supplier', supplier),

            MessageHandler(Filters.regex('^(' + msg_text.channel_set['uz'][1] + ')$'), admin_back),
            MessageHandler(Filters.text, channel_add_url)
        ],
        state.channel_add_id: [
            CommandHandler('start', start),
            CommandHandler('help', help),
            CommandHandler('admin', admin),
            MessageHandler(Filters.regex('^(' + msg_text.channel_set['uz'][1] + ')$'), admin_back),
            MessageHandler(Filters.text, channel_add_id)
        ],
        state.add_category: [
            CommandHandler('start', start),
            CommandHandler('help', help),
            CommandHandler('admin', admin),
            MessageHandler(Filters.regex('^(' + msg_text.channel_set['uz'][1] + ')$'), admin_back),
            MessageHandler(Filters.text, get_category),
        ],
        state.category_image_uz: [
            CommandHandler('start', start),
            CommandHandler('help', help),
            CommandHandler('admin', admin),
            MessageHandler(Filters.regex('^(' + msg_text.channel_set['uz'][1] + ')$'), admin_back),
            MessageHandler(Filters.photo, get_category_image_uz),
        ],
        state.category_image_ru: [
            CommandHandler('start', start),
            CommandHandler('help', help),
            CommandHandler('admin', admin),
            MessageHandler(Filters.regex('^(' + msg_text.channel_set['uz'][1] + ')$'), admin_back),
            MessageHandler(Filters.photo, get_category_image_ru),
        ],
        state.del_category: [
            CommandHandler('start', start),
            CommandHandler('help', help),
            CommandHandler('admin', admin),
            MessageHandler(Filters.regex('^(' + msg_text.channel_set['uz'][1] + ')$'), admin_back),
            MessageHandler(Filters.text, category_del),
        ],

        state.add_product: [
            CommandHandler('start', start),
            CommandHandler('help', help),
            CommandHandler('admin', admin),
            MessageHandler(Filters.regex('^(' + msg_text.channel_set['uz'][1] + ')$'), admin_back),
            MessageHandler(Filters.text, get_product_name),
        ],
        state.add_product_content: [
            CommandHandler('start', start),
            CommandHandler('help', help),
            CommandHandler('admin', admin),
            MessageHandler(Filters.regex('^(' + msg_text.channel_set['uz'][1] + ')$'), admin_back),
            MessageHandler(Filters.text, get_product_content),
        ],
        state.add_product_price: [
            CommandHandler('start', start),
            CommandHandler('help', help),
            CommandHandler('admin', admin),
            MessageHandler(Filters.regex('^(' + msg_text.channel_set['uz'][1] + ')$'), admin_back),
            MessageHandler(Filters.text, add_product_price),
        ],
        state.add_product_discount: [
            CommandHandler('start', start),
            CommandHandler('help', help),
            CommandHandler('admin', admin),
            MessageHandler(Filters.regex('^(' + msg_text.channel_set['uz'][1] + ')$'), admin_back),
            MessageHandler(Filters.text, add_product_discount),
        ],
        state.add_product_photo: [
            CommandHandler('start', start),
            CommandHandler('help', help),
            CommandHandler('admin', admin),
            MessageHandler(Filters.regex('^(' + msg_text.channel_set['uz'][1] + ')$'), admin_back),
            MessageHandler(Filters.photo, add_product_photo),
        ],
        state.add_product_category: [
            CommandHandler('start', start),
            CommandHandler('help', help),
            CommandHandler('admin', admin),
            CallbackQueryHandler(add_product_category),
        ],
        state.product_yes_no: [
            CommandHandler('start', start),
            CommandHandler('help', help),
            CommandHandler('admin', admin),
            MessageHandler(Filters.regex('^(' + msg_text.yes_no['uz'][0] + ')$'), product_yes_size),
            MessageHandler(Filters.regex('^(' + msg_text.yes_no['uz'][1] + ')$'), product_no_size),
        ],
        state.product_size_name: [
            CommandHandler('start', start),
            CommandHandler('help', help),
            CommandHandler('admin', admin),
            MessageHandler(Filters.regex('^(' + msg_text.channel_set['uz'][1] + ')$'), admin_back),
            MessageHandler(Filters.text, product_size_name),
        ],
        state.product_size_price: [
            CommandHandler('start', start),
            CommandHandler('help', help),
            CommandHandler('admin', admin),
            MessageHandler(Filters.regex('^(' + msg_text.channel_set['uz'][1] + ')$'), admin_back),
            MessageHandler(Filters.text, product_size_price),
        ],
        state.del_product: [
            CommandHandler('start', start),
            CommandHandler('help', help),
            CommandHandler('admin', admin),
            MessageHandler(Filters.regex('^(' + msg_text.channel_set['uz'][1] + ')$'), admin_back),
            MessageHandler(Filters.text, product_del),
        ],
        state.add_admin: [
            CommandHandler('start', start),
            CommandHandler('help', help),
            CommandHandler('admin', admin),
            MessageHandler(Filters.regex('^(' + msg_text.channel_set['uz'][1] + ')$'), admin_back),
            MessageHandler(Filters.text, get_admin_chat_id),
        ],
        state.del_admin: [
            CommandHandler('start', start),
            CommandHandler('help', help),
            CommandHandler('admin', admin),
            MessageHandler(Filters.regex('^(' + msg_text.channel_set['uz'][1] + ')$'), admin_back),
            MessageHandler(Filters.text, admin_del),
        ],
        state.add_supplier: [
            CommandHandler('start', start),
            CommandHandler('help', help),
            CommandHandler('admin', admin),
            MessageHandler(Filters.regex('^(' + msg_text.channel_set['uz'][1] + ')$'), admin_back),
            MessageHandler(Filters.text, get_supplier_chat_id),
        ],
        state.add_supplier_name: [
            CommandHandler('start', start),
            CommandHandler('help', help),
            CommandHandler('admin', admin),
            MessageHandler(Filters.regex('^(' + msg_text.channel_set['uz'][1] + ')$'), admin_back),
            MessageHandler(Filters.text, get_supplier_name),
        ],
        state.add_supplier_phone: [
            CommandHandler('start', start),
            CommandHandler('help', help),
            CommandHandler('admin', admin),
            MessageHandler(Filters.regex('^(' + msg_text.channel_set['uz'][1] + ')$'), admin_back),
            MessageHandler(Filters.text, get_supplier_phone),
        ],
        state.del_supplier: [
            CommandHandler('start', start),
            CommandHandler('help', help),
            CommandHandler('admin', admin),
            MessageHandler(Filters.regex('^(' + msg_text.channel_set['uz'][1] + ')$'), admin_back),
            MessageHandler(Filters.text, supplier_del),
        ],
        state.adversting: [
            CommandHandler('start', start),
            CommandHandler('help', help),
            CommandHandler('admin', admin),
            MessageHandler(Filters.regex('^(' + msg_text.channel_set['uz'][1] + ')$'), admin_back),
            MessageHandler(Filters.all, get_adversting),
        ],
        state.unfinished_orders: [
            CommandHandler('start', start),
            CommandHandler('help', help),
            CommandHandler('admin', admin),
            MessageHandler(Filters.regex('^(' + msg_text.channel_set['uz'][1] + ')$'), admin_back),
            MessageHandler(Filters.text, get_order_id),
        ],
        state.choose_order_supplier: [
            CommandHandler('start', start),
            CommandHandler('help', help),
            CommandHandler('admin', admin),
            MessageHandler(Filters.regex('^(' + msg_text.channel_set['uz'][1] + ')$'), admin_back),
            CallbackQueryHandler(choose_order_supplier),
        ],
        state.manager: [
            CommandHandler('start', start),
            CommandHandler('help', help),
            CommandHandler('admin', admin),
            CommandHandler('boss', admin),
            MessageHandler(Filters.regex('^(' + msg_text.manager['uz'][0] + ')$'), finished_orders),
            MessageHandler(Filters.regex('^(' + msg_text.manager['uz'][1] + ')$'), subscriber_stats),
            MessageHandler(Filters.regex('^(' + msg_text.manager['uz'][2] + ')$'), report_by_day),
        ],
        state.manager_report_by_day: [
            CommandHandler('start', start),
            CommandHandler('help', help),
            CommandHandler('admin', admin),
            CommandHandler('boss', admin),
            MessageHandler(Filters.regex('^(' + msg_text.manager['uz'][0] + ')$'), finished_orders),
            MessageHandler(Filters.regex('^(' + msg_text.manager['uz'][1] + ')$'), subscriber_stats),
            MessageHandler(Filters.regex('^(' + msg_text.manager['uz'][2] + ')$'), report_by_day),
            MessageHandler(Filters.text, input_report_by_day),
        ],
        state.location: [
            CommandHandler('start', start),
            CommandHandler('help', help),
            CommandHandler('admin', admin),
            CommandHandler('boss', manager),
            MessageHandler(Filters.regex('^(' + msg_text.get_location['uz'][0] + ')$'), user_locations),
            MessageHandler(Filters.regex('^(' + msg_text.get_location['ru'][0] + ')$'), user_locations),
            MessageHandler(Filters.regex('^(' + msg_text.get_location['en'][0] + ')$'), user_locations),
            MessageHandler(Filters.regex('^(' + msg_text.get_location['uz'][1] + ')$'), get_user_only_location),
            MessageHandler(Filters.regex('^(' + msg_text.get_location['ru'][1] + ')$'), get_user_only_location),
            MessageHandler(Filters.regex('^(' + msg_text.get_location['en'][1] + ')$'), get_user_only_location),
            MessageHandler(Filters.regex('^(' + msg_text.get_location['uz'][2] + ')$'), back),
            MessageHandler(Filters.regex('^(' + msg_text.get_location['ru'][2] + ')$'), back),
            MessageHandler(Filters.regex('^(' + msg_text.get_location['en'][2] + ')$'), back),
            MessageHandler(Filters.location, get_user_location),
        ],
        state.confirm_location: [
            CommandHandler('start', start),
            CommandHandler('help', help),
            CommandHandler('admin', admin),
            CommandHandler('boss', manager),
            MessageHandler(Filters.regex('^(' + msg_text.confirmation['uz'][0] + ')$'), confirm_location),
            MessageHandler(Filters.regex('^(' + msg_text.confirmation['ru'][0] + ')$'), confirm_location),
            MessageHandler(Filters.regex('^(' + msg_text.confirmation['en'][0] + ')$'), confirm_location),
            MessageHandler(Filters.regex('^(' + msg_text.confirmation['uz'][1] + ')$'), back),
            MessageHandler(Filters.regex('^(' + msg_text.confirmation['ru'][1] + ')$'), back),
            MessageHandler(Filters.regex('^(' + msg_text.confirmation['en'][1] + ')$'), back),
        ],
        state.choose_location: [
            CommandHandler('start', start),
            CommandHandler('help', help),
            CommandHandler('admin', admin),
            CommandHandler('boss', manager),
            CallbackQueryHandler(choose_location),
        ],
        state.choose_category: [
            CommandHandler('start', start),
            CommandHandler('help', help),
            CommandHandler('admin', admin),
            CommandHandler('boss', manager),
            CallbackQueryHandler(choose_category),
        ],
        state.choose_product: [
            CommandHandler('start', start),
            CommandHandler('help', help),
            CommandHandler('admin', admin),
            CommandHandler('boss', manager),
            CallbackQueryHandler(choose_product),
        ],
        state.choose_product_size: [
            CommandHandler('start', start),
            CommandHandler('help', help),
            CommandHandler('admin', admin),
            CommandHandler('boss', manager),
            CallbackQueryHandler(choose_product_size),
        ],
        state.sell_product_count: [
            CommandHandler('start', start),
            CommandHandler('help', help),
            CommandHandler('admin', admin),
            CommandHandler('boss', manager),
            CallbackQueryHandler(sell_product_count),
        ],
        state.my_cart: [
            CommandHandler('start', start),
            CommandHandler('help', help),
            CommandHandler('admin', admin),
            CommandHandler('boss', manager),
            CallbackQueryHandler(cart),
        ],
        state.index_cart: [
            CommandHandler('start', start),
            CommandHandler('help', help),
            CommandHandler('admin', admin),
            CommandHandler('boss', manager),
            CallbackQueryHandler(index_cart),
        ],
        state.settings: [
            CommandHandler('start', start),
            CommandHandler('help', help),
            CommandHandler('admin', admin),
            MessageHandler(Filters.regex('^(' + msg_text.settings['uz'][0] + ')$'), change_language_settings),
            MessageHandler(Filters.regex('^(' + msg_text.settings['ru'][0] + ')$'), change_language_settings),
            MessageHandler(Filters.regex('^(' + msg_text.settings['uz'][1] + ')$'), change_phone_number),
            MessageHandler(Filters.regex('^(' + msg_text.settings['ru'][1] + ')$'), change_phone_number),
            MessageHandler(Filters.regex('^(' + msg_text.settings['uz'][2] + ')$'), back),
            MessageHandler(Filters.regex('^(' + msg_text.settings['ru'][2] + ')$'), back),
        ],
        state.change_language: [
            CommandHandler('start', start),
            CommandHandler('help', help),
            CommandHandler('admin', admin),
            CallbackQueryHandler(change_language_settings_text),
        ],
        state.change_phone_number: [
            CommandHandler('start', start),
            CommandHandler('help', help),
            CommandHandler('admin', admin),
            MessageHandler(Filters.regex('^(' + msg_text.settings['uz'][2] + ')$'), back),
            MessageHandler(Filters.regex('^(' + msg_text.settings['ru'][2] + ')$'), back),
            MessageHandler(Filters.contact, change_phone_number_text),
            MessageHandler(Filters.text, change_phone_number_text),
        ],

        state.supplier: [
            CommandHandler('start', start),
            CommandHandler('help', help),
            CommandHandler('admin', admin),
            CommandHandler('supplier', supplier),
            MessageHandler(Filters.regex('^(' + msg_text.supplier['uz'][0] + ')$'), unfinished_orders),
            MessageHandler(Filters.regex('^(' + msg_text.supplier['ru'][0] + ')$'), unfinished_orders),
            MessageHandler(Filters.regex('^(' + msg_text.supplier['uz'][1] + ')$'), my_finished_orders),
            MessageHandler(Filters.regex('^(' + msg_text.supplier['ru'][1] + ')$'), my_finished_orders),
        ],
        state.supplier_order: [
            CommandHandler('start', start),
            CommandHandler('help', help),
            CommandHandler('admin', admin),
            CommandHandler('supplier', supplier),
            MessageHandler(Filters.regex('^(' + msg_text.supplier['uz'][0] + ')$'), unfinished_orders),
            MessageHandler(Filters.regex('^(' + msg_text.supplier['ru'][0] + ')$'), unfinished_orders),
            MessageHandler(Filters.regex('^(' + msg_text.supplier['uz'][1] + ')$'), my_finished_orders),
            MessageHandler(Filters.regex('^(' + msg_text.supplier['ru'][1] + ')$'), my_finished_orders),
            MessageHandler(Filters.text, supplier_order),
        ],
        state.supplier_order_status: [
            CommandHandler('start', start),
            CommandHandler('help', help),
            CommandHandler('admin', admin),
            CommandHandler('supplier', supplier),
            MessageHandler(Filters.regex('^(' + msg_text.supplier_order['uz'][4] + ')$'), supplier),
            MessageHandler(Filters.text, supplier_order_status),
        ],
        state.get_photo: [
            CommandHandler('start', start),
            CommandHandler('help', help),
            CommandHandler('admin', admin),
            CommandHandler('supplier', supplier),
            MessageHandler(Filters.regex('^(' + msg_text.settings['uz'][2] + ')$'), back),
            MessageHandler(Filters.regex('^(' + msg_text.settings['ru'][2] + ')$'), back),
            MessageHandler(Filters.photo, get_photo_and_send_file_id),
        ],
    },
    fallbacks=[CommandHandler('start', start),
               CommandHandler('help', help),
               CommandHandler('admin', admin), ]
)

dispatcher.add_handler(all_handler)
