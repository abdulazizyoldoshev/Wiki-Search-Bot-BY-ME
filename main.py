from telegram.ext import Updater, Dispatcher, CommandHandler, CallbackContext, MessageHandler
from settings import settings
from telegram.update import Update
from telegram.ext.filters import Filters
import requests


updater = Updater(token=settings.TELEGRAM_TOKEN)


def start(update: Update, context: CallbackContext):
    update.message \
        .reply_text("Assalomu alaykum! Wikipediadan m'alumot "
                    "qidiruvchi botga hush kelibsiz! Biror nima "
                    "izlash uchun /search va so'rovingizni yozing. "
                    "Misol uchun ( /search Pubg Mobile )")


def search(update: Update, context: CallbackContext):
    args = context.args

    if len(args) == 0:
        update.message\
            .reply_text("Hech bo'lmasa, nimadir kiriting. "
                        "Misol uchun ( /search O'zbekiston )")
    else:
        search_text = ''.join(args)
        response = requests.get('https://uz.wikipedia.org/w/api.php', {
            'action': 'opensearch',
            'search': search_text,
            'limit': 1,
            'namespace': 0,
            'format': 'json',
        })

        result = response.json()
        link = result[3]

        if len(link):
            update.message \
                .reply_text("Sizning so'rovingiz bo'yicha havola:" + link[0])
        else:
            update.message \
                .reply_text("Afsus sizning so'rovingiz bo'yicha hech narsa yo'q")


dispatcher = updater.dispatcher
dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler('search', search))
dispatcher.add_handler(MessageHandler(Filters.all, start))



updater.start_polling()
updater.idle()
