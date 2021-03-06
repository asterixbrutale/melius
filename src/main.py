import os
import telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyMarkup,\
                    ForceReply, PhotoSize, Video
from telegram.ext import Updater, MessageHandler, CommandHandler, CallbackQueryHandler, Filters, BaseFilter

from config import *
from bot_functions import *

from json_functions import *
dict_0 = readJsonFile(cfg.PATH_DICT)
dict_1 =dict_0["italian"]

def start(bot,update):
    chat_id = update.message.chat_id
    bot.send_message(chat_id,"Welcome to @thinkmelius_bot we are official MELIUS evergreen bot!\nUse /commands for show commands")
    #bot.sendPhoto(chat_id,photo=open("../image/logo.png",'rb'))
    set_language(bot,update)

def set_language(bot,update):
    chat_id = update.message.chat_id
    bot.send_message(chat_id,"Choose your language for start!",reply_markup=set_language_keyboard())
    bot.sendPhoto(chat_id,photo=open("../image/igotrade.jpg",'rb'))

def main_menu(bot, update):
    chat_id = update.message.chat_id
    global dict_1
    lang=searchLangOfChatId(chat_id)
    
    #Menu under insert text field
    if(lang=="italian"):
            bot.sendMessage(chat_id,text_main_menu_1_ita,reply_markup = main_menu_keyboard())
    if(lang=="english"):
            bot.sendMessage(chat_id,text_main_menu_1_eng,reply_markup = main_menu_keyboard())
                    
def list_commands_menu(bot, update):
    chat_id = update.message.chat_id
    text="/language\n/menu\n/igotrade\n/ibo\n/admin\n"
    bot.send_message(chat_id,text)
    
def callback_handler(bot,update):
    query = update.callback_query
    message = query.message
    chat_id = message.chat_id
    global dict_1
        
    if(query.data=='set_language_it'):
        addUserJsonFile(chat_id,"italian")
        dict_1 = getDictByLanguage("italian")
        bot.send_message(chat_id,dict_1["language_setted"])
        bot.deleteMessage(chat_id, message.message_id)
        main_menu(bot,query)
    
    if(query.data=='set_language_eng'):
        addUserJsonFile(chat_id,"english")
        dict_1 = getDictByLanguage("english")
        bot.send_message(chat_id,dict_1["language_setted"])
        bot.deleteMessage(chat_id, message.message_id)
        main_menu(bot,query)

    if(query.data=='Link_2'):
        if(lang=="italian"):
            bot.send_message(chat_id,testo_50k_ita)
        if(lang=="english"):
            bot.send_message(chat_id,testo_50k_eng)  
    if(query.data=='Link_5'):
        bot.send_message(chat_id,"Link_5")
    bot.answerCallbackQuery(query.id)
    
def message_callback_handler(bot, update):
    message_text = update.message.text
    chat_id = update.message.chat_id
    global dict_1
    lang=searchLangOfChatId(chat_id)
    reply = update.message.reply_to_message

    if(lang!=None):
        dict_1=dict_0[lang]
    else:
        addUserJsonFile(chat_id,"italian") #non dovrebbe mai succedere perche il caso è gia gestito all inizio
        dict_1=dict_0["italian"]
        
    if(message_text == dict_1["main_menu"][0]): #igotrade
        if(lang=="italian"):
            bot.send_message(chat_id,text_sub_menu_1_ita)
            bot.send_message(chat_id,link_youtube_sm4_ita)
            bot.send_message(chat_id,testo2_igotrade_ita)
            bot.send_message(chat_id,video_node)
        if(lang=="english"):
            bot.send_message(chat_id,text_sub_menu_1_eng)
            bot.send_message(chat_id,link_youtube_sm4_eng)
            bot.send_message(chat_id,testo2_igotrade_eng)
            bot.send_message(chat_id,video_node)
        #bot.send_message(chat_id,dict_1["calculator_menu"][0],reply_markup=sub_menu_calculator_keyboard())
    
    if(message_text == dict_1["main_menu"][1]): #50k real
        if(lang=="italian"):
            bot.send_message(chat_id,text_sub_menu_2_ita)
            bot.sendPhoto(chat_id,photo=open("../image/50k.jpeg",'rb'))
            bot.send_message(chat_id,testo_50k_ita)
        if(lang=="english"):
            bot.send_message(chat_id,text_sub_menu_2_eng)
            bot.sendPhoto(chat_id,photo=open("../image/50k.jpeg",'rb'))
            bot.send_message(chat_id,testo_50k_eng)
    if(message_text == dict_1["main_menu"][2]): #network
        if(lang=="italian"):
            #bot.send_message(chat_id,link_youtube_sm3_ita)
            bot.send_message(chat_id,testo_network_ita)
            bot.send_document(chat_id,document=open(doc_sm1_ita,'rb'))
            bot.send_message(chat_id,presentazione_ita)
            #bot.send_document(chat_id,document=open(doc_sm3_2_ita,'rb'))
        if(lang=="english"):
            #bot.send_message(chat_id,link_youtube_sm3_eng)
            bot.send_message(chat_id,testo_network_eng)
            bot.send_document(chat_id,document=open(doc_sm3_1_eng,'rb'))
            bot.send_message(chat_id,presentazione_eng)
            #bot.send_document(chat_id,document=open(doc_sm3_2_eng,'rb'))

    if(message_text == dict_1["main_menu"][3]): #contatti
        
        if(lang=="italian"):
            bot.send_message(chat_id,message_text,reply_markup=sub_menu_contact_keyboard())
            bot.send_message(chat_id,testo_contatti)
            bot.send_message(chat_id,link_youtube_sm3_eng)
        if(lang=="english"):
            bot.send_message(chat_id,message_text,reply_markup=sub_menu_contact_keyboard())
            bot.send_message(chat_id,link_youtube_sm3_eng)
        
    
    if(message_text == dict_1["main_menu"][4]): #report
        if(lang=="italian"):
            bot.send_message(chat_id,text_sub_menu_5_ita,reply_markup=sub_menu_keyboard("5"))
        if(lang=="english"):
            bot.send_message(chat_id,text_sub_menu_5_eng,reply_markup=sub_menu_keyboard("5"))
    
    if(message_text == dict_1["go_back"]):
        main_menu(bot,update)
    
    if(message_text == dict_1["calculator_menu"][0]): #calcolatore
        bot.send_message(chat_id,dict_1["calculator_menu"][1],reply_markup=ForceReply(force_reply=True))
        
    if(reply!=None): #calcolatore
        if(reply.text == dict_1["calculator_menu"][1]):
            split_str = message_text.split(" ")
            if(len(split_str) == 2):
                if((split_str[0].isdigit()) & ((split_str[1] == dict_1["calculator_menu"][3]) | (split_str[1] == dict_1["calculator_menu"][4]) | (split_str[1] == dict_1["calculator_menu"][5]))):
                    if(float(split_str[0])<500):
                        bot.send_message(chat_id,dict_1["calculator_menu"][6])
                        bot.send_message(chat_id,dict_1["calculator_menu"][1],reply_markup=ForceReply(force_reply=True))
                    else:
                        bot.send_message(chat_id,split_str[0]+" "+split_str[1])
                        if (split_str[1] == dict_1["calculator_menu"][3]):
                            risk = 0
                        if (split_str[1] == dict_1["calculator_menu"][4]):
                            risk = 1
                        if (split_str[1] == dict_1["calculator_menu"][5]):
                            risk = 2
                        pip_value = calculator(float(split_str[0]),risk)
                        bot.send_message(chat_id,dict_1["calculator_menu"][7]+": "+str(round(pip_value,2))+" euro")
						bot.sendMessage(chat_id,"Main menu",reply_markup = main_menu_keyboard())
            else:
                bot.send_message(chat_id,dict_1["calculator_menu"][2])
                bot.send_message(chat_id,dict_1["calculator_menu"][1],reply_markup=ForceReply(force_reply=True))
    
    if(message_text == dict_1["contact_menu"][0]):
        bot.send_message(chat_id,link_gruppo_telegram),
        bot.send_message(link_gruppo_telegram1)
    if(message_text == dict_1["contact_menu"][1]):
        bot.send_message(chat_id,link_gruppo_whatsapp)
    if(message_text == dict_1["contact_menu"][2]):
        bot.send_message(chat_id,telegram_contatto)
        
def set_language_keyboard():
    keyboard = [[InlineKeyboardButton('Italiano', callback_data='set_language_it'),
              InlineKeyboardButton('English', callback_data='set_language_eng')]]
    return InlineKeyboardMarkup(keyboard)

def main_menu_keyboard():
    main_menu_buttons = [[(dict_1["main_menu"][0]), 
               (dict_1["main_menu"][1])],
              [(dict_1["main_menu"][2]),
               (dict_1["main_menu"][3])],
              [(dict_1["main_menu"][4]),(dict_1["calculator_menu"][0])]]
    main_menu_keyboard = ReplyKeyboardMarkup(main_menu_buttons, resize_keyboard = True)
    return main_menu_keyboard

def sub_menu_keyboard(data):
    keyboard = [[InlineKeyboardButton('HOW ?', callback_data='Link_'+data)]]
    return InlineKeyboardMarkup(keyboard)

def sub_menu_contact_keyboard():
    keyboard = [[(dict_1["contact_menu"][0]), 
               (dict_1["contact_menu"][1]),
               (dict_1["contact_menu"][2])],
              [dict_1["go_back"]]]
    return ReplyKeyboardMarkup(keyboard)

def sub_menu_calculator_keyboard():
    keyboard = [[(dict_1["calculator_menu"][0])],[dict_1["go_back"]]]
    return ReplyKeyboardMarkup(keyboard)

bot = telegram.Bot(TOKEN)

def main():
    #variabile TOKEN presente nel file config
    updater = Updater(TOKEN, request_kwargs={'read_timeout': 20, 'connect_timeout': 20})
    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('language', set_language))
    dp.add_handler(CommandHandler('menu', main_menu))
    dp.add_handler(CommandHandler('commands', list_commands_menu))
    dp.add_handler(MessageHandler(Filters.text, message_callback_handler))
    

    dp.add_handler(CallbackQueryHandler(callback_handler))

    updater.start_polling()
    updater.idle()

main()