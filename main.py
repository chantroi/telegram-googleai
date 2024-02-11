from hydrogram import Client, filters
from environ import api_id, api_hash, bot_token
from hydrogram.enums import ChatAction
from res import pro, pro_vision
import os, sys

app = Client("Google AI", api_id, api_hash, bot_token=bot_token, in_memory=True)

@app.on_message(filters.command(["start","help"]) & filters.private)
async def basic(c, m):
    await m.reply_chat_action(ChatAction.TYPING)
    await m.reply("Hello, __--Welcome to Unofficial Google AI--__", quote=True)
    
@app.on_message(filters.command("refresh") & filters.user(5665225938))
def refresh_chat(c, m):
    os.execl(sys.executable, sys.executable, *sys.argv)
    
def photo_message(_, __, m):
    return m.reply_to_message and m.reply_to_message.photo
    
@app.on_message((filters.mentioned | (filters.private & filters.user(5665225938))) & (filters.photo | filters.create(photo_message)))
async def pro_vision_model(c, m):
    await m.reply_chat_action(ChatAction.TYPING)
    try:
        if m.reply_to_message:
            text = m.text
            photo = await c.download_media(m.reply_to_message, in_memory=True)
        else:
            raise
    except Exception as e:
        print(e)
        text = m.caption
        photo = await c.download_media(m, in_memory=True)
    if not text:
        text = "Phân tích ảnh này"
    if text.startswith("@"):
        text = text.split(" ", 1)[1]
    try:
        res = pro_vision(photo, text)
        await m.reply_chat_action(ChatAction.TYPING)
        await m.reply(res, quote=True)
    except Exception as e:
        await m.reply(str(e), quote=True)
    
@app.on_message((filters.mentioned | (filters.private & filters.user(5665225938))) & filters.text)
async def pro_model(c, m):
    await m.reply_chat_action(ChatAction.TYPING)
    if m.text.startswith("@"):
        text = m.text.split(" ", 1)[1]
    else:
        text = m.text
    try:
        res = pro(text)
        await m.reply_chat_action(ChatAction.TYPING)
        await m.reply(res, quote=True)
    except Exception as e:
        await m.reply(str(e), quote=True)
    
app.run()