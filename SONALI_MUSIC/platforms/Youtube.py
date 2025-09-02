import asyncio
import os
import re
import json
from typing import Union
import requests
import yt_dlp
from pyrogram.enums import MessageEntityType
from pyrogram.types import Message
from youtubesearchpython.__future__ import VideosSearch
from SONALI_MUSIC.utils.database import is_on_off
from SONALI_MUSIC.utils.formatters import time_to_seconds
import aiohttp
import config
from config import NEW_API_URL  # Only this is used now


def cookie_txt_file():
    cookie_dir = f"{os.getcwd()}/cookies"
    cookies_files = [f for f in os.listdir(cookie_dir) if f.endswith(".txt")]
    return os.path.join(cookie_dir, random.choice(cookies_files))


async def download_song(link: str):
    video_id = link.split('v=')[-1].split('&')[0]
    download_folder = "downloads"

    for ext in ["mp3", "m4a", "webm"]:
        file_path = f"{download_folder}/{video_id}.{ext}"
        if os.path.exists(file_path):
            return file_path

    # Try NEW API first
    new_song_url = f"{NEW_API_URL}/song/{video_id}"
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(new_song_url) as response:
                if response.status == 200:
                    data = await response.json()
                    download_url = data.get("link") or data.get("url")
                    if download_url:
                        return await download_file(session, download_url, video_id, data)
                else:
                    print(f"NEW_API failed with status: {response.status}")
        except Exception as e:
            print(f"NEW_API exception: {e}")

    print("Both API methods failed, falling back to yt-dlp cookies method")
    return None


async def download_file(session, download_url, video_id, data):
    try:
        file_format = data.get("format", "mp3")
        file_extension = file_format.lower()
        file_name = f"{video_id}.{file_extension}"
        download_folder = "downloads"
        os.makedirs(download_folder, exist_ok=True)
        file_path = os.path.join(download_folder, file_name)

        async with session.get(download_url) as file_response:
            with open(file_path, 'wb') as f:
                while True:
                    chunk = await file_response.content.read(8192)
                    if not chunk:
                        break
                    f.write(chunk)
        return file_path
    except Exception as e:
        print(f"Download error: {e}")
        return None


async def check_file_size(link):
    async def get_format_info(link):
        proc = await asyncio.create_subprocess_exec(
            "yt-dlp", "--cookies", cookie_txt_file(), "-J", link,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await proc.communicate()
        if proc.returncode != 0:
            print(f'Error:\n{stderr.decode()}')
            return None
        return json.loads(stdout.decode())

    def parse_size(formats):
        return sum(f.get('filesize', 0) for f in formats)

    info = await get_format_info(link)
    if not info:
        return None
    return parse_size(info.get('formats', []))


async def shell_cmd(cmd):
    proc = await asyncio.create_subprocess_shell(
        cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE,
    )
    out, err = await proc.communicate()
    return out.decode() if out else err.decode()


class YouTubeAPI:
    def __init__(self):
        self.base = "https://www.youtube.com/watch?v="
        self.regex = r"(?:youtube\.com|youtu\.be)"
        self.status = "https://www.youtube.com/oembed?url="
        self.listbase = "https://youtube.com/playlist?list="

    async def exists(self, link: str, videoid: Union[bool, str] = None):
        if videoid:
            link = self.base + link
        return bool(re.search(self.regex, link))

    async def url(self, message_1: Message) -> Union[str, None]:
        messages = [message_1]
        if message_1.reply_to_message:
            messages.append(message_1.reply_to_message)

        for message in messages:
            if message.entities:
                for entity in message.entities:
                    if entity.type == MessageEntityType.URL:
                        text = message.text or message.caption
                        return text[entity.offset : entity.offset + entity.length]
            elif message.caption_entities:
                for entity in message.caption_entities:
                    if entity.type == MessageEntityType.TEXT_LINK:
                        return entity.url
        return None

    async def details(self, link: str, videoid: Union[bool, str] = None):
        if videoid:
            link = self.base + link
        if "&" in link:
            link = link.split("&")[0]
        results = VideosSearch(link, limit=1)
        for result in (await results.next())["result"]:
            title = result["title"]
            duration_min = result["duration"]
            duration_sec = int(time_to_seconds(duration_min or "0"))
            thumbnail = result["thumbnails"][0]["url"].split("?")[0]
            vidid = result["id"]
        return title, duration_min, duration_sec, thumbnail, vidid

    async def download(
        self, link: str, mystic,
        video: Union[bool, str] = None,
        videoid: Union[bool, str] = None,
        songaudio: Union[bool, str] = None,
        songvideo: Union[bool, str] = None,
        format_id: Union[bool, str] = None,
        title: Union[bool, str] = None,
    ) -> str:
        if videoid:
            link = self.base + link

        loop = asyncio.get_running_loop()

        def audio_dl():
            opts = {
                "format": "bestaudio/best",
                "outtmpl": "downloads/%(id)s.%(ext)s",
                "geo_bypass": True,
                "nocheckcertificate": True,
                "quiet": True,
                "cookiefile": cookie_txt_file(),
                "no_warnings": True,
            }
            x = yt_dlp.YoutubeDL(opts)
            info = x.extract_info(link, False)
            filepath = os.path.join("downloads", f"{info['id']}.{info['ext']}")
            if os.path.exists(filepath):
                return filepath
            x.download([link])
            return filepath

        def video_dl():
            opts = {
                "format": "(bestvideo[height<=?720][ext=mp4])+bestaudio[ext=m4a]",
                "outtmpl": "downloads/%(id)s.%(ext)s",
                "geo_bypass": True,
                "nocheckcertificate": True,
                "quiet": True,
                "cookiefile": cookie_txt_file(),
                "no_warnings": True,
            }
            x = yt_dlp.YoutubeDL(opts)
            info = x.extract_info(link, False)
            filepath = os.path.join("downloads", f"{info['id']}.{info['ext']}")
            if os.path.exists(filepath):
                return filepath
            x.download([link])
            return filepath

        if songvideo or songaudio:
            downloaded_file = await download_song(link)
            if downloaded_file:
                return downloaded_file
            return await loop.run_in_executor(None, audio_dl)

        elif video:
            if await is_on_off(1):
                file_size = await check_file_size(link)
                if not file_size:
                    return
                if file_size / (1024 * 1024) > 250:
                    print("File size too large.")
                    return None
                return await loop.run_in_executor(None, video_dl)
            else:
                proc = await asyncio.create_subprocess_exec(
                    "yt-dlp", "--cookies", cookie_txt_file(), "-g", "-f", "best[height<=?720][width<=?1280]",
                    link, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE,
                )
                stdout, stderr = await proc.communicate()
                if stdout:
                    return stdout.decode().split("\n")[0]
                return await loop.run_in_executor(None, video_dl)

        else:
            downloaded_file = await download_song(link)
            if downloaded_file:
                return downloaded_file
            return await loop.run_in_executor(None, audio_dl)
