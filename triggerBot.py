#!/usr/bin/python
# -*- coding: utf-8 -*-
import telebot
import logging
import psycopg2     #sql

from model import addTrigger, delTrigger, listTriggers
import config       #config.py

#CRITICAL > ERROR > WARNING > INFO
logging.basicConfig(format=u'%(filename)s[LINE:%(lineno)-3s]# %(levelname)-5s [%(asctime)s] %(message)s', level=logging.INFO)
logging.info("bot loaded")

bot = telebot.TeleBot(config.token)

@bot.message_handler(content_types = ["text"])
def messageHandler(message):
    if message.chat.type == "supergroup" or message.chat.type == "group":

        #Adding new trigger
        if message.text == "/add_trigger":
            bot.send_message(message.chat.id, "to add a trigger reply to the desired message <b>/add_trigger {trigger}</b>", parse_mode = "html")
        elif message.text.startswith("/add_trigger "):
            if message.reply_to_message:
                addTrigger()
                logging.info("new trigger - \"" + message.text.replace("/add_trigger ", "") + "\"")
                bot.send_message(message.chat.id, "trigger <b>\"" + message.text.replace("/add_trigger ", "") + "\"</b> has been added", parse_mode = "html")
            else:
                bot.send_message(message.chat.id, "you should <b>reply</b> to the desired message", parse_mode = "html")
                logging.info("can't add trigger(not reply)")

        #delete trigger
        elif message.text == "/del_trigger":
            bot.send_message(message.chat.id, "to delete trigger <b>/del_trigger {trigger}</b>", parse_mode = "html")
        elif message.text.startswith("/del_trigger "):
            delTrigger()
            logging.info("trigger - \"" + message.text.replace("/del_trigger ", "") + "\" has been deleted")
            bot.send_message(message.chat.id, "trigger <b>\"" + message.text.replace("/del_trigger ", "") + "\"</b> has been deleted", parse_mode = "html")

        #list of triggers
        elif message.text == "/list_of_triggers":
            bot.send_message(message.chat.id, "<b>list of triggers:</b>\n\n" + str(listTriggers()), parse_mode = "html")



if __name__ == '__main__':
     bot.polling(none_stop=True)
