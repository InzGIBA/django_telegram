from django.views import View
from django.conf import settings
from django.http import HttpResponse 
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from .models import PersonalUser, Message
import telebot
import logging
import time
import jwt
import os


@method_decorator(csrf_exempt, name='dispatch')
class BotView(View):
    def get(self, request):
        return HttpResponse('get')
    
    @csrf_exempt
    def post(self, request):
        print(request)
        if request.headers.get('content-type') == 'application/json':
            json_string = request.body.decode('utf-8')
            update = telebot.types.Update.de_json(json_string)
            bot.process_new_updates([update])
        return HttpResponse('post')


API_TOKEN = ''
WEBHOOK_HOST = ''
WEBHOOK_PORT = 443
WEBHOOK_SSL_CERT = os.path.join(settings.BASE_DIR, 'webhook_cert.pem')
WEBHOOK_SSL_PRIV = os.path.join(settings.BASE_DIR, 'webhook_pkey.pem')
WEBHOOK_URL_BASE = "https://%s:%s" % (WEBHOOK_HOST, WEBHOOK_PORT)
WEBHOOK_URL_PATH = "/%s/" % (API_TOKEN)

logger = telebot.logger
telebot.logger.setLevel(logging.INFO)

bot = telebot.TeleBot(API_TOKEN)


@bot.message_handler(regexp='^[A-Za-z0-9-_=]+\.[A-Za-z0-9-_=]+\.?[A-Za-z0-9-_.+/=]*$')
def send_welcome(message):
    try:
        result_message = jwt.decode(message.text, 'super_secret_key', algorithms=['HS256'])
        print(result_message)
    except Exception as e:
        print(e)
        temp = "Ошибка определения токена"
    else:
        bot.delete_message(message.chat.id, message.message_id)
        try:
            person = PersonalUser.objects.get(pk=result_message.get('user_id'))
            person.telegram_id = message.from_user.id
            person.save()
        except Exception as e:
            print(e)
            temp = "Ошибка определения пользователя"
        else:
            temp = "Токен успешно установлен"
    bot.send_message(message.chat.id, temp)


@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.reply_to(message, ("Пришлите пожалуйста JWT токен, для дальнейшей работы"))


status = bot.remove_webhook()
time.sleep(1)
status = bot.set_webhook(url=WEBHOOK_URL_BASE + WEBHOOK_URL_PATH) #, certificate=open(WEBHOOK_SSL_CERT, 'r'))


def send_message(chat_id, text):
    bot.send_message(chat_id, text)