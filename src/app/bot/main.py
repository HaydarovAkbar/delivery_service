from telegram import Bot
from telegram.ext import Dispatcher, CommandHandler, MessageHandler, Filters, ConversationHandler, \
    CallbackQueryHandler
from decouple import config
from django.conf import settings
from .methods.base import start, language, send_feedback, back, \
    help, add_to_channel, get_contact_text, get_contact
from .methods.admin import admin, search_user, admin_back, channel_one_set, get_unfinished_orders, \
    get_finished_orders, get_photo
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

        MessageHandler(Filters.regex('^(' + msg_text.back['uz'] + ')$'), back),
        MessageHandler(Filters.regex('^(' + msg_text.back['ru'] + ')$'), back),
        MessageHandler(Filters.regex('^(' + msg_text.back['en'] + ')$'), back),
    ],
    states={
        state.language: [CommandHandler('start', start),
                         CommandHandler('help', help),
                         CommandHandler('admin', admin),

                         CallbackQueryHandler(language, pattern='^(uz|ru|en)$')],
        state.contact: [CommandHandler('start', start),
                        CommandHandler('help', help),
                        CommandHandler('admin', admin),
                        MessageHandler(Filters.contact, get_contact),
                        MessageHandler(Filters.text, get_contact_text),
                        ],
        state.main: [
            CommandHandler('start', start),
            CommandHandler('help', help),
            CommandHandler('admin', admin),

            MessageHandler(Filters.regex('^(' + msg_text.back['uz'] + ')$'), back),
            MessageHandler(Filters.regex('^(' + msg_text.back['ru'] + ')$'), back),
            MessageHandler(Filters.regex('^(' + msg_text.back['en'] + ')$'), back),
        ],
        state.feedback: [
            CommandHandler('start', start),
            CommandHandler('help', help),
            CommandHandler('admin', admin),

            MessageHandler(Filters.regex('^(' + msg_text.back['uz'] + ')$'), back),
            MessageHandler(Filters.regex('^(' + msg_text.back['ru'] + ')$'), back),
            MessageHandler(Filters.regex('^(' + msg_text.back['en'] + ')$'), back),
            MessageHandler(Filters.all, send_feedback)],
        state.check_channel: [
            CommandHandler('start', start),
            CommandHandler('help', help),
            CommandHandler('admin', admin),
            CallbackQueryHandler(add_to_channel), ],

        state.admin: [
            CommandHandler('start', start),
            CommandHandler('help', help),
            CommandHandler('admin', admin),

            MessageHandler(Filters.regex('^(' + msg_text.admin['ru'][14] + ')$'), get_unfinished_orders),
            MessageHandler(Filters.regex('^(' + msg_text.admin['ru'][15] + ')$'), get_finished_orders),
            MessageHandler(Filters.regex('^(' + msg_text.admin['ru'][16] + ')$'), get_photo),
        ],
        state.search_user: [
            CommandHandler('start', start),
            CommandHandler('help', help),
            CommandHandler('admin', admin),

            MessageHandler(Filters.regex('^(' + msg_text.back['uz'] + ')$'), admin_back),
            MessageHandler(Filters.regex('^(' + msg_text.back['ru'] + ')$'), admin_back),
            MessageHandler(Filters.regex('^(' + msg_text.back['en'] + ')$'), admin_back),
            MessageHandler(Filters.text, search_user)
        ],

        state.channel_set: [
            CommandHandler('start', start),
            CommandHandler('help', help),
            CommandHandler('admin', admin),

            MessageHandler(Filters.regex('^(' + msg_text.channel_set['uz'][1] + ')$'), admin_back),
            MessageHandler(Filters.text, channel_one_set)
        ],
    },
    fallbacks=[CommandHandler('start', start),
               CommandHandler('help', help),
               CommandHandler('admin', admin), ]
)

dispatcher.add_handler(all_handler)
