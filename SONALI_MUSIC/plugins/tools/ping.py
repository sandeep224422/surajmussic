from datetime import datetime
from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from SONALI_MUSIC import app
from SONALI_MUSIC.core.call import Sona
from SONALI_MUSIC.utils import bot_sys_stats
from SONALI_MUSIC.utils.decorators.language import language
from SONALI_MUSIC.utils.inline import supp_markup
from SONALI_MUSIC.utils.inline import close_markup
from config import BANNED_USERS
import aiohttp
import asyncio
from io import BytesIO
from PIL import Image, ImageEnhance  # Add these imports

async def make_carbon(code):
    url = "https://carbonara.solopov.dev/api/cook"
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json={"code": code}) as resp:
            image = BytesIO(await resp.read())

    # Open the image using PIL
    carbon_image = Image.open(image)

    # Increase brightness
    enhancer = ImageEnhance.Brightness(carbon_image)
    bright_image = enhancer.enhance(1.7)  # Adjust the enhancement factor as needed

    # Save the modified image to BytesIO object with increased quality
    output_image = BytesIO()
    bright_image.save(output_image, format='PNG', quality=95)  # Adjust quality as needed
    output_image.name = "carbon.png"
    return output_image

@app.on_message(filters.command("ping", prefixes=["/"]) & ~BANNED_USERS)
@language
async def ping_com(client, message: Message, _):
    PING_IMG_URL = "https://files.catbox.moe/hae7d5.jpg"
    captionss = "**ᴘɪɴɢɪɴɢ ᴏᴜʀ sᴇʀᴠᴇʀ ᴡᴀɪᴛ.**"
    response = await message.reply_photo(PING_IMG_URL, caption=(captionss))
    await asyncio.sleep(1)
    await response.edit_caption("**ᴘɪηɢɪηɢ ᴏᴜʀ sєʀᴠєʀ ᴡᴧɪᴛ.**")
    await asyncio.sleep(1)
    await response.edit_caption("**ᴘɪηɢɪηɢ ᴏᴜʀ sєʀᴠєʀ ᴡᴧɪᴛ..**")
    await asyncio.sleep(1)
    await response.edit_caption("**ᴘɪηɢɪηɢ ᴏᴜʀ sєʀᴠєʀ ᴡᴧɪᴛ...**")
    await asyncio.sleep(1.5)
    await response.edit_caption("**ᴘɪηɢɪηɢ ᴏᴜʀ sєʀᴠєʀ ᴡᴧɪᴛ....**")
    await asyncio.sleep(2)
    await response.edit_caption("**ᴘɪηɢɪηɢ ᴏᴜʀ sєʀᴠєʀ ᴡᴧɪᴛ.....**")
    await asyncio.sleep(2)
    await response.edit_caption("**𝐁𝐑𝐀𝐇𝐈𝐗 sʏsᴛєϻ ᴅᴧᴛᴧ ᴧηᴧʟʏsєᴅ sᴜᴄᴄєssғᴜʟʟʏ !**")
    await asyncio.sleep(3)
    await response.edit_caption("**𝐁𝐑𝐀𝐇𝐈𝐗 sʏsᴛєϻ ᴧηᴧʟʏsєᴅ ᴅᴧᴛᴧ ᴘʟєᴧsє ᴡᴧɪᴛ...**")
    start = datetime.now()
    pytgping = await Sona.ping()
    UP, CPU, RAM, DISK = await bot_sys_stats()
    resp = (datetime.now() - start).microseconds / 1000
    text =  _["ping_2"].format(resp, app.name, UP, RAM, CPU, DISK, pytgping)
    carbon = await make_carbon(text)
    captions = "**ㅤ  ❍ ᴘɪηɢ...ᴘσηɢ...ᴘɪηɢ\nㅤ  ❍ ᴅɪηɢ...ᴅσηɢ...ᴅɪηɢ**"
    await message.reply_photo((carbon), caption=captions,
    reply_markup=InlineKeyboardMarkup(
            [
                [
            InlineKeyboardButton(
                text=_["S_B_1"],
                url=f"https://t.me/{app.username}?startgroup=true",
            )
        
        ],
        [
            InlineKeyboardButton(
                text="• ʜᴇʟᴘ •", url=f"https://t.me/brahix_support",
            ),
            InlineKeyboardButton(
                text="• ᴍᴏʀᴇ •", url=f"https://t.me/brahix_support",
            )
        ],
        [
            InlineKeyboardButton(
                text="• 𝐁𝐑𝐀𝐇𝐈𝐗 •", url=f"https://t.me/{app.username}?start=help"
            )
        ],
    ]
    ),
        )
    await response.delete()

    close_button = InlineKeyboardButton("๏ ᴄʟᴏsᴇ ๏", callback_data="close_data")
    inline_keyboard = InlineKeyboardMarkup([[close_button]])

@app.on_callback_query(filters.regex("^close_data"))
async def close_callback(_, query):
    chat_id = query.message.chat.id
    await query.message.delete()
