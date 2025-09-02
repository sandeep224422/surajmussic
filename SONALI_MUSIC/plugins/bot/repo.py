from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from SONALI_MUSIC import app
from config import BOT_USERNAME
from SONALI_MUSIC.utils.errors import capture_err
import httpx 
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

start_txt = """**
<u>❃ 𝚆𝙴𝙻𝙲𝙾𝙼𝙴 𝚃𝙾 𝚁𝙴𝙿𝙾𝚂 𝚂𝙴𝙲𝚃𝙸𝙾𝙽 ❃</u>
 
✼ ʀєᴘᴏ ᴛᴏ ηʜɪ ϻɪʟєɢᴧ ʏʜᴧ
 
❉ ᴘᴧʜʟє ᴘᴧᴘᴧ ʙσʟ ʀєᴘᴏ ᴏᴡηєʀ ᴋᴏ 

✼ || [Dᴇᴠɪʟ](https://t.me/about_brahixs) ||
 
❊ ʀᴜη 24x7 ʟᴧɢ ϝʀєє ᴡɪᴛʜσᴜᴛ sᴛσᴘ**
"""




@app.on_message(filters.command("repo"))
async def start(_, msg):
    buttons = [
        [ 
          InlineKeyboardButton("✙ ᴧᴅᴅ ϻє вᴧʙʏ ✙", url=f"https://t.me/{BOT_USERNAME}?startgroup=true")
        ],
        [
          InlineKeyboardButton("• ʜєʟᴘ •", url="https://t.me/about_brahixs"),
          InlineKeyboardButton("• 𝛅ᴜᴘᴘσʀᴛ •", url="https://t.me/about_brahixs"),
          ],
[
InlineKeyboardButton("• ϻᴧɪη ʙσᴛ •", url=f"https://t.me/Komal_music_bot"),

        ]]
    
    reply_markup = InlineKeyboardMarkup(buttons)
    
    await msg.reply_photo(
        photo="https://files.catbox.moe/mhia7u.jpg",
        caption=start_txt,
        reply_markup=reply_markup
    )
