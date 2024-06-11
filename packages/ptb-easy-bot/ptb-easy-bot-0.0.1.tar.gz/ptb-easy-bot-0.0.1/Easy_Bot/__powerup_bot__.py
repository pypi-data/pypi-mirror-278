from telegram import Update , Bot
from telegram.ext import Application  
from telegram.ext import CommandHandler as commnders
from telegram.ext import MessageHandler as Messengers
from telegram.ext import CallbackQueryHandler as Callbacker
from telegram.ext import filters as Filters

import asyncio
import os 

PORT = int(os.environ.get('PORT', '8443'))


LOGO = """........................................
.#####...####...##...##...####...#####..
.##..##.##..##..###.###..##..##..##..##.
.#####..######..##.#.##..##..##..##..##.
.##.....##..##..##...##..##..##..##..##.
.##.....##..##..##...##...####...#####..
........................................    
   ├ ᴄᴏᴘʏʀɪɢʜᴛ © 𝟸𝟶𝟸𝟹-𝟸𝟶𝟸𝟺 ᴘᴀᴍᴏᴅ ᴍᴀᴅᴜʙᴀsʜᴀɴᴀ. ᴀʟʟ ʀɪɢʜᴛs ʀᴇsᴇʀᴠᴇᴅ.
   ├ ʟɪᴄᴇɴsᴇᴅ ᴜɴᴅᴇʀ ᴛʜᴇ  ɢᴘʟ-𝟹.𝟶 ʟɪᴄᴇɴsᴇ.
   └ ʏᴏᴜ ᴍᴀʏ ɴᴏᴛ ᴜsᴇ ᴛʜɪs ғɪʟᴇ ᴇxᴄᴇᴘᴛ ɪɴ ᴄᴏᴍᴘʟɪᴀɴᴄᴇ ᴡɪᴛʜ ᴛʜᴇ ʟɪᴄᴇɴsᴇ.
"""

async def set_webhook(webhook_url,TOKEN):
     bot = Bot(TOKEN)
     await bot.set_webhook(webhook_url + "/" + TOKEN)


def _powerup_bot_(TOKEN: str , Handlers: dict , Webhook_url: str) -> None:
    print(LOGO)
    app = Application.builder().token(TOKEN).build()

    for handler , command_and_function in Handlers.items():
        for command , function in dict(command_and_function).items():
            if handler == "Error":
                app.add_error_handler(function)
            
            elif command != None:
                app.add_handler(handler(command , function))

            else:    
                app.add_handler(handler(function))
    
    print("Bot Started !")
    if Webhook_url != None:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(set_webhook(Webhook_url,TOKEN))
        app.run_webhook(port=PORT,listen="0.0.0.0",webhook_url=Webhook_url)
    else:
        app.run_polling()
    
    
