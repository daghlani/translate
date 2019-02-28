#!/home/elenoon/my/venv_python3.5/bin/python
# coding=utf-8
"""Simple Bot to Reply to Bale messages."""
from balebot.models.messages import TextMessage, TemplateMessageButton, TemplateMessage
from balebot.filters import TextFilter, PhotoFilter, TemplateResponseFilter
from sqlalchemy.ext.declarative import declarative_base
from balebot.models.base_models import Peer
from balebot.handlers import MessageHandler
from sqlalchemy.orm import sessionmaker
from balebot.updater import Updater
from sqlalchemy import *
import configparser
import asyncio
import logging
import pr_me
import os


configfile = '/home/elenoon/my/translate/config.properties'
config = configparser.RawConfigParser()
config.read(configfile)

bot_token = config.get('public_config', 'bot_token')
# Bale Bot Authorization Token
updater = Updater(token=bot_token,
                  loop=asyncio.get_event_loop())
# Define dispatcher
dispatcher = updater.dispatcher


users_name = config.get('public_config', 'users_name')
suggestions_name = config.get('public_config', 'suggestions_name')


db_name = config.get('public_config', 'db_name')
db_user = config.get('public_config', 'db_user')
db_pass = config.get('public_config', 'db_pass')
db_host = config.get('public_config', 'db_host')


db = create_engine('postgresql://' + db_user + ':' + db_pass + '@' + db_host + '/' + db_name, echo=False)


Sesseion = sessionmaker(db)

metadata = MetaData()

session = Sesseion()

Base = declarative_base()


class User(Base):
    __tablename__ = users_name
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, unique=True)
    user_accessHash = Column(String)

    def __repr__(self):
        return "<User(user_id='%s', user_accessHash='%s')>" % (
            self.user_id, self.user_accessHash)


users = Table(users_name, metadata,
              Column('id', Integer, primary_key=True, autoincrement=True),
              Column('user_id', Integer, unique=True),
              Column('user_accessHash', String(60))
              )


class Suggest(Base):
    __tablename__ = suggestions_name
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer)
    user_accessHash = Column(String)
    suggest = Column(String(length=1000, convert_unicode='UTF-8'))

    def __repr__(self):
        return "<User(user_id='%s', user_accessHash='%s', Suggest='%s')>" % (
            self.user_id, self.user_accessHash, self.suggest)


suggestions = Table(suggestions_name, metadata,
                    Column('id', Integer, primary_key=True, autoincrement=True),
                    Column('user_id', Integer),
                    Column('user_accessHash', String),
                    Column('suggest', String(length=1000, convert_unicode='UTF-8'))
                    )

if db.has_table(users) is not True:
    users.create(bind=db)
    logging.info('%s db created.' % users_name)

if db.has_table(suggestions) is not True:
    suggestions.create(bind=db)
    logging.info('%s db created.' % suggestions_name)




# Both of success and failure functions are optional
def success(response, user_data):
    print("success : ", response)
    print(user_data)


def failure(response, user_data):
    print("failure : ", response)
    print(user_data)


# coding=utf-8
from googletrans import Translator

translator = Translator()

admin_user_id = config.get('public_config', 'admin_user_id')
admin_user_accessHash = config.get('public_config', 'admin_user_accessHash')
# chanel_user_id = config.get('public_config', 'chanel_user_id')
# chanel_user_accessHash = config.get('public_config', 'chanel_user_accessHash')

btn_1 = TemplateMessageButton(text=pr_me.texts['advertise_form_button_name'], value="/form", action=1)
btn_2 = TemplateMessageButton(text=pr_me.texts['send_advertise_button_name'], value="send_advertise", action=1)
btn_3 = TemplateMessageButton(text=pr_me.texts['suggestions_button_name'], value="suggest", action=1)
btn_4 = TemplateMessageButton(text=pr_me.texts['about_button_name'], value="about", action=1)
btn_5 = TemplateMessageButton(text=pr_me.texts['sent_to_chanel_button_name'], value="sent_to_chanel", action=1)
btn_6 = TemplateMessageButton(text=pr_me.texts['the_rules_button'], value="the_rules", action=1)
btn_7 = TemplateMessageButton(text=pr_me.texts['other_language_button'], value="other_language", action=1)
btn_cancel = TemplateMessageButton(text=pr_me.texts['cancel_button'], value="/cancel", action=0)

LANGUAGES = {
    'af': 'afrikaans',
    'sq': 'albanian',
    'am': 'amharic',
    'ar': 'arabic',
    'hy': 'armenian',
    'az': 'azerbaijani',
    'eu': 'basque',
    'be': 'belarusian',
    'bn': 'bengali',
    'bs': 'bosnian',
    'bg': 'bulgarian',
    'ca': 'catalan',
    'ceb': 'cebuano',
    'ny': 'chichewa',
    'zh-cn': 'chinese (simplified)',
    'zh-tw': 'chinese (traditional)',
    'co': 'corsican',
    'hr': 'croatian',
    'cs': 'czech',
    'da': 'danish',
    'nl': 'dutch',
    'en': 'english',
    'eo': 'esperanto',
    'et': 'estonian',
    'tl': 'filipino',
    'fi': 'finnish',
    'fr': 'french',
    'fy': 'frisian',
    'gl': 'galician',
    'ka': 'georgian',
    'de': 'german',
    'el': 'greek',
    'gu': 'gujarati',
    'ht': 'haitian creole',
    'ha': 'hausa',
    'haw': 'hawaiian',
    'iw': 'hebrew',
    'hi': 'hindi',
    'hmn': 'hmong',
    'hu': 'hungarian',
    'is': 'icelandic',
    'ig': 'igbo',
    'id': 'indonesian',
    'ga': 'irish',
    'it': 'italian',
    'ja': 'japanese',
    'jw': 'javanese',
    'kn': 'kannada',
    'kk': 'kazakh',
    'km': 'khmer',
    'ko': 'korean',
    'ku': 'kurdish (kurmanji)',
    'ky': 'kyrgyz',
    'lo': 'lao',
    'la': 'latin',
    'lv': 'latvian',
    'lt': 'lithuanian',
    'lb': 'luxembourgish',
    'mk': 'macedonian',
    'mg': 'malagasy',
    'ms': 'malay',
    'ml': 'malayalam',
    'mt': 'maltese',
    'mi': 'maori',
    'mr': 'marathi',
    'mn': 'mongolian',
    'my': 'myanmar (burmese)',
    'ne': 'nepali',
    'no': 'norwegian',
    'ps': 'pashto',
    'fa': 'persian',
    'pl': 'polish',
    'pt': 'portuguese',
    'pa': 'punjabi',
    'ro': 'romanian',
    'ru': 'russian',
    'sm': 'samoan',
    'gd': 'scots gaelic',
    'sr': 'serbian',
    'st': 'sesotho',
    'sn': 'shona',
    'sd': 'sindhi',
    'si': 'sinhala',
    'sk': 'slovak',
    'sl': 'slovenian',
    'so': 'somali',
    'es': 'spanish',
    'su': 'sundanese',
    'sw': 'swahili',
    'sv': 'swedish',
    'tg': 'tajik',
    'ta': 'tamil',
    'te': 'telugu',
    'th': 'thai',
    'tr': 'turkish',
    'uk': 'ukrainian',
    'ur': 'urdu',
    'uz': 'uzbek',
    'vi': 'vietnamese',
    'cy': 'welsh',
    'xh': 'xhosa',
    'yi': 'yiddish',
    'yo': 'yoruba',
    'zu': 'zulu',
    'fil': 'Filipino',
    'he': 'Hebrew'
}

@dispatcher.message_handler(filters=[TextFilter(keywords=["/start", "/START", "/Start", "start", "START", "Start"]),
                                     TemplateResponseFilter(keywords=["menu"])])
def echo(bot, update):
    user_id = update.get_effective_user().peer_id
    access_hash = update.get_effective_user().access_hash

    user_id_db = session.query(users).filter(users.c.user_id == user_id).count()
    if user_id_db < 1:
        user = User(user_id=user_id, user_accessHash=access_hash)
        session.add(user)
        session.commit()
        logging.info('user added id: %s, acceshash: %s' % (user_id, access_hash))

    user_peer = update.get_effective_user()
    general_message = TextMessage(pr_me.texts['welcome'])
    if update.get_effective_user().peer_id == admin_user_id:
        # btn_list = [btn_1, btn_2, btn_3, btn_4, btn_5, btn_6]
        btn_list = [btn_1, btn_2, btn_3, btn_4, btn_5, btn_6, btn_7]
    else:
        # btn_list = [btn_1, btn_2, btn_3, btn_4, btn_6]
        btn_list = [btn_7]
    template_message = TemplateMessage(general_message=general_message, btn_list=btn_list)
    bot.send_message(template_message, user_peer, success_callback=success, failure_callback=failure)

@dispatcher.message_handler(TemplateResponseFilter(keywords=["other_language"]))
def get_language(bot, update):
    message = TextMessage(pr_me.texts['get_language'])
    btn_list = []
    btn_list.append(btn_cancel)
    for i in LANGUAGES:
        btn_list.append(TemplateMessageButton(text=LANGUAGES[i], value=i, action=0))
    template_message = TemplateMessage(general_message=message, btn_list=btn_list)
    user_peer = update.get_effective_user()
    bot.send_message(template_message, user_peer, success_callback=success, failure_callback=failure)
    dispatcher.register_conversation_next_step_handler(update, [MessageHandler(TemplateResponseFilter(), get_text),
                                                                MessageHandler(
                                                                    TemplateResponseFilter(keywords='/cancel'),
                                                                    function_cancel)])


def get_text(bot, update):
    message = TextMessage(pr_me.texts['get_text'])
    dest_lang = update.get_effective_message().text
    dispatcher.set_conversation_data(update=update, key="dest_lang", value=dest_lang)
    user_peer = update.get_effective_user()
    btn_list = [TemplateMessageButton(text=pr_me.texts['menu_button'], value="menu", action=0)]
    template_message = TemplateMessage(general_message=message, btn_list=btn_list)
    bot.send_message(template_message, user_peer, success_callback=success, failure_callback=failure)
    dispatcher.register_conversation_next_step_handler(update, [MessageHandler(TextFilter(), translate_text),
                                                                MessageHandler(
                                                                    TemplateResponseFilter(keywords='/cancel'),
                                                                    function_cancel)])

def translate_text(bot, update):
    dest_lang = dispatcher.get_conversation_data(update=update, key="dest_lang")
    src_text = update.get_effective_message().text
    dest_text = translator.translate(src_text, dest=dest_lang).text
    user_peer = update.get_effective_user()
    message = TextMessage(dest_text)
    btn_list = [TemplateMessageButton(text=pr_me.texts['menu_button'], value="menu", action=0)]
    bot.send_message(message, user_peer, success_callback=success, failure_callback=failure)
    dispatcher.finish_conversation(update)

@dispatcher.default_handler()  # filter text the client enter to bot
def echo(bot, update):
    data = update.get_effective_message().text
    print (data)
    src_lang_def = config.get('public_config', 'src_lang_def')
    dest_lang_def = config.get('public_config', 'dest_lang_def')
    word_lang = translator.detect(data).lang
    print ('========================================================================================================')
    print (word_lang)
    print ('========================================================================================================')
    if word_lang == src_lang_def:
        dest_to_translate = dest_lang_def
    elif word_lang == dest_lang_def:
        dest_to_translate = src_lang_def
    else:
        dest_to_translate = dest_lang_def

    a = translator.translate(data, dest=dest_to_translate)
    message = TextMessage(a.text)
    # Send a message to client
    user_peer = update.get_effective_user()
    bot.send_message(message, user_peer, success_callback=success, failure_callback=failure)


def function_cancel(bot, update):
    user_peer = update.get_effective_user()
    btn_list = [TemplateMessageButton(text=pr_me.texts['menu_button'], value="menu", action=0)]
    message = TextMessage(pr_me.texts['canceled'])
    template_message = TemplateMessage(general_message=message, btn_list=btn_list)
    bot.send_message(template_message, user_peer, success_callback=success, failure_callback=failure)
    dispatcher.finish_conversation(update)


# Run the bot!
updater.run()
