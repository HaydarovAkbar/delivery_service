import time

from telegram import Update
from telegram.ext import CallbackContext
from app.bot.messages.main import MessageText as msg_text
from app.bot.keyboards.base import Keyboards as kb, number as num
from app.bot.states import States as state
from app.models import TGUsers, Caption, Channel, Admin, Products, ProductSize, Level


def add_to_channel(update: Update, context: CallbackContext):
    query = update.callback_query
    user_lang = update.effective_user.language_code if update.effective_user.language_code in ['uz', 'ru',
                                                                                               'en'] else 'en'
    channel = Channel.objects.filter(status=True)
    left_channel = []
    for ch in channel:
        try:
            a = context.bot.get_chat_member(chat_id=ch.channel_id, user_id=update.effective_user.id)
            if a.status == 'left':
                left_channel.append(ch)
        except Exception as e:
            print(e)
    if left_channel:
        query.answer(text=msg_text.add_to_channel.get(user_lang), show_alert=True)
        return state.check_channel
    query.delete_message()
    return start(update, context)


def start(update: Update, context: CallbackContext):
    all_channel = Channel.objects.filter(status=True)
    user_lang = update.effective_user.language_code
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
        if not user.language:
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
    user.level = Level.objects.first()
    user.save()
    query.delete_message(timeout=0.2)
    user_lang = user.language if user.language in ['uz', 'ru', 'en'] else 'en'
    context.bot.send_message(chat_id=query.message.chat_id, text=msg_text.base.get(user_lang), parse_mode='HTML')
    return state.main


def back(update: Update, context: CallbackContext):
    pass


def my_profile(update: Update, context: CallbackContext):
    user_db = TGUsers.objects.get(chat_id=update.effective_user.id)
    user_lang = user_db.language if user_db.language in ['uz', 'ru', 'en'] else 'en'

    user_info = f"""

"""