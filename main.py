# ===============================================
import os
import dotenv
import clients
import coders
from pathlib import Path
from telegram.ext import (Updater,
                          CommandHandler,
                          ConversationHandler,
                          MessageHandler,
                          Filters)

import db_api

dotenv.load_dotenv(Path('venv', '.env'))
bot_token = os.environ['PINKY']


def start(update, _):
    username = update.message.chat.username
    if db_api.is_contractor_verified(username):
        update.message.reply_text('welcome, dear coder /common for coding')
    elif db_api.is_subscription_active(username):
        update.message.reply_text('welcome, dear client type /begin for cooperate')
    else:
        update.message.reply_text('you have to contact with owners ')


updater = Updater(token=bot_token)
dispatcher = updater.dispatcher
start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

client_conversation_handler = ConversationHandler(
    entry_points=[CommandHandler('begin', clients.start_client_talk),
                  CommandHandler('create', clients.create_order),
                  CommandHandler('active', clients.expose_active_order),
                  CommandHandler('accepted', clients.accept_order)],
    states={
        clients.C_1: [CommandHandler('create', clients.create_order),
                      CommandHandler('active', clients.expose_active_order),
                      CommandHandler('accepted', clients.accept_order)],
        clients.C_2: [MessageHandler(Filters.text & (~Filters.command), clients.send_order),
                      CommandHandler('begin', clients.start_client_talk),
                      CommandHandler('accepted', clients.accept_order)
                      ],
        clients.C_3: [MessageHandler(Filters.text & (~Filters.command), clients.work_with_order),
                      CommandHandler('begin', clients.start_client_talk),
                      CommandHandler('accepted', clients.accept_order)],
        clients.C_4: [MessageHandler(Filters.text & (~Filters.command), clients.message_for_coder),
                      CommandHandler('active', clients.expose_active_order),
                      CommandHandler('accepted', clients.accept_order)],
        clients.C_5: [MessageHandler(Filters.text & (~Filters.command), clients.send_credits),
                      CommandHandler('begin', clients.start_client_talk),
                      CommandHandler('accepted', clients.accept_order)],
        clients.C_6: [MessageHandler(Filters.text & (~Filters.command), clients.closing_order),
                      CommandHandler('begin', clients.start_client_talk),
                      CommandHandler('accepted', clients.accept_order)]
    },
    fallbacks=[CommandHandler('cancel', clients.client_cancel)]
)
dispatcher.add_handler(client_conversation_handler)

coder_conversation_handler = ConversationHandler(
    entry_points=[
        CommandHandler('common', coders.start_coder_talk),
        CommandHandler('salary', coders.salary),
        CommandHandler('order', coders.order),
        CommandHandler('summary', coders.summary),
        CommandHandler('orders', coders.orders),
        CommandHandler('active_orders', coders.active_orders),
        CommandHandler('available', coders.get_avaliable_orders)

    ],
    states={
        coders.C_1: [CommandHandler('salary', coders.salary),
                     CommandHandler('orders', coders.orders),
                     CommandHandler('common', coders.start_coder_talk)],

        coders.C_2: [CommandHandler('order', coders.order),
                     CommandHandler('summary', coders.summary),
                     CommandHandler('orders', coders.orders),
                     CommandHandler('common', coders.start_coder_talk)],

        coders.C_3: [CommandHandler('active_orders', coders.active_orders),
                     CommandHandler('available', coders.get_avaliable_orders),
                     CommandHandler('salary', coders.salary),
                     CommandHandler('common', coders.start_coder_talk)],

        coders.C_4: [MessageHandler(Filters.text & (~Filters.command), coders.work_with_order),
                     CommandHandler('orders', coders.orders),
                     CommandHandler('common', coders.start_coder_talk),
                     CommandHandler('active_orders', coders.active_orders)],

        coders.C_5: [
            CommandHandler('submit', coders.submit_order),
            CommandHandler('get_admin', coders.get_admin),
            CommandHandler('question', coders.ask_question),
            CommandHandler('common', coders.start_coder_talk),
            CommandHandler('active_orders', coders.active_orders)
        ],
        coders.C_6: [MessageHandler(Filters.text & (~Filters.command), coders.message_for_client),
                     CommandHandler('common', coders.start_coder_talk),
                     CommandHandler('active_orders', coders.active_orders)],
        coders.C_7: [MessageHandler(Filters.text & (~Filters.command), coders.choose_order),
                     CommandHandler('orders', coders.orders),
                     CommandHandler('common', coders.start_coder_talk),
                     CommandHandler('active_orders', coders.active_orders)
                     ],
        coders.C_8: [MessageHandler(Filters.text & (~Filters.command), coders.send_estimate_data_confirmation_order),
                     CommandHandler('available', coders.get_avaliable_orders),
                     CommandHandler('common', coders.start_coder_talk),
                     CommandHandler('active_orders', coders.active_orders)
                     ]
    },
    fallbacks=[CommandHandler('cancel', coders.coder_cancel)]
)
dispatcher.add_handler(coder_conversation_handler)

updater.start_polling()
