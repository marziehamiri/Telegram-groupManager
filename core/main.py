
import telebot
import os
import logging
import requests
from telebot.types import ChatPermissions

logger = telebot.logger
telebot.logger.setLevel(logging.INFO)

API_TOKEN = 'token'
bot = telebot.TeleBot(API_TOKEN)

badwordlist = ["badword1","badword2","badword3"]
def has_bad_words(text):
    for bad_word in badwordlist:
        if bad_word in text:
            return True
    return False
warnings = []
@bot.message_handler(func= lambda messsage:True)
def message_handle(message):
    if has_bad_words(message.text):
        if str(message.from_user.id) in warnings:
            warnings[message.from_user.id] += 1
        else:
            warnings[message.from_user.id] = 1
        if warnings[message.from_user.id] > 3 :
            bot.kick_chat_member(message.chat.id,message.from_user.id)

        if warnings[str(message.from_user.id)] > 3:
            bot.kick_chat_member(message.chat.id,message.from_user.id)
            bot.send_message(message.chat.id,f"user {message.from_user.username} has been kicked out because of breaking bad word rule" )
        else:
            bot.reply_to(message,f"please dont use bad words, this is your {warnings[str(message.from_user.id)]} warnings, after third warning you will be kicked out")
    



def is_admin(message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    user_info = bot.get_chat_member(chat_id,user_id)
    #logger.info(user_info)
    return user_info.status in ["creator","administrator"]


@bot.message_handler(func=is_admin,commands=["restrict"])
def handle_restriction(message):
    permissions = ChatPermissions (
        can_send_message = False,
        can_send_audios=False,
        can_send_documents=False,
        can_send_photos=False,
        can_send_videos=False,
        can_send_video_notes=False,
        can_send_voice_notes=False,
        can_send_polls=False,
        can_send_other_messages=False,
        can_add_web_page_previews=False,
        can_invite_users=False
    )
    bot.set_chat_permissions(message.chat.id,permissions=permissions)
    logger.info("aplying restricyion")
    bot.send_message(message.chat.id,"night mode activated")
    

@bot.message_handler(func=is_admin,commands=["unrestrict"])
def handle_unrestriction(message):
    permissions = ChatPermissions (
            can_send_message = True,
            can_send_audios=True,
            can_send_documents=True,
            can_send_photos=True,
            can_send_videos=True,
            can_send_video_notes=True,
            can_send_voice_notes=True,
            can_send_polls=True,
            can_send_other_messages=True,
            can_add_web_page_previews=True,
            can_invite_users=True
        )
    bot.set_chat_permissions(message.chat.id,permissions=permissions)
    logger.info("aplying unrestricyion")
    bot.send_message(message.chat.id,"night mode deactivated")

bot.infinity_polling(skip_pending=True)
