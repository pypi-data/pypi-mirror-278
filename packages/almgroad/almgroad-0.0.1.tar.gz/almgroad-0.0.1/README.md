python3 -m pip install --index-url https://test.pypi.org/simple/ --no-deps example-package-YOUR-USERNAME-HEREhttps://pypi.org/project/almgroad0770a/import requests
import telebot
from time import sleep 
import threading 
id = ايدي الحساب او القناة او المجموعة 
bot = telebot.TeleBot("توكن_البوت")
is_error = False 
def yyy():
    global is_error
    while True:
        r = requests.get('https://tk.alfenganexchange.com/RequestBuyUsd/getbranch').json()
        if 'error' in r:
            if not is_error:
                bot.send_message(id, 'تم نفاذ الحصة')
                is_error = True
        else:
            if is_error:
                bot.send_message(id, 'تم نزول الحصة')
                is_error = False
        sleep(1)

@bot.message_handler(commands=['start'])
def sss(message):
    bot.reply_to(message ,'اهلًا عزيزي سيتم ارسال رسالة لك عندما ينفتح الموقع')
    threading.Thread(target=yyy).start()

bot.infinity_polling()