from telegram import Bot
from telegram.ext import Dispatcher, CommandHandler, MessageHandler, Filters, ConversationHandler, \
    CallbackQueryHandler, InlineQueryHandler
from decouple import config
from django.conf import settings
from .methods.base import start, language, add_to_channel, back, my_profile
from .methods.admin import admin, search_user, admin_back, channel_one_set
import logging
from .states import States as state
from .messages.main import KeyboardText as msg_text

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.WARNING)

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
        state.main: [
            CommandHandler('start', start),
            CommandHandler('help', help),
            CommandHandler('admin', admin),

            MessageHandler(Filters.regex('^(' + msg_text.base['uz'][0] + ')$'), my_profile),
            MessageHandler(Filters.regex('^(' + msg_text.base['uz'][1] + ')$'), back),
            MessageHandler(Filters.regex('^(' + msg_text.base['uz'][2] + ')$'), back),
            MessageHandler(Filters.regex('^(' + msg_text.base['uz'][3] + ')$'), back),

            MessageHandler(Filters.regex('^(' + msg_text.base['ru'][0] + ')$'), my_profile),
            MessageHandler(Filters.regex('^(' + msg_text.base['ru'][1] + ')$'), back),
            MessageHandler(Filters.regex('^(' + msg_text.base['ru'][2] + ')$'), back),
            MessageHandler(Filters.regex('^(' + msg_text.base['ru'][3] + ')$'), back),

            MessageHandler(Filters.regex('^(' + msg_text.base['en'][0] + ')$'), my_profile),
            MessageHandler(Filters.regex('^(' + msg_text.base['en'][1] + ')$'), back),
            MessageHandler(Filters.regex('^(' + msg_text.base['en'][2] + ')$'), back),
            MessageHandler(Filters.regex('^(' + msg_text.base['en'][3] + ')$'), back),
        ],
        state.feedback: [
            CommandHandler('start', start),
            CommandHandler('help', help),
            CommandHandler('admin', admin),

            MessageHandler(Filters.regex('^(' + msg_text.back['uz'] + ')$'), back),
            MessageHandler(Filters.regex('^(' + msg_text.back['ru'] + ')$'), back),
            MessageHandler(Filters.regex('^(' + msg_text.back['en'] + ')$'), back), ],
        state.check_channel: [
            CommandHandler('start', start),
            CommandHandler('help', help),
            CommandHandler('admin', admin),
            CallbackQueryHandler(add_to_channel),
        ],
    },
    fallbacks=[CommandHandler('start', start),
               CommandHandler('help', help),
               CommandHandler('admin', admin), ]
)

dispatcher.add_handler(all_handler)
