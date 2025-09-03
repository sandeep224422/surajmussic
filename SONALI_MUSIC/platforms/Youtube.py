import asyncio
import os
import re
import json
import random
from typing import Union
import requests
import yt_dlp
import aiohttp

# API URL directly in code
NEW_API_URL = "https://apikeyy-zeta.vercel.app/api"


def cookie_txt_file():
    cookie_dir = f"{os.getcwd()}/cookies"
    if not os.path.exists(cookie_dir):
        return None
    cookies_files = [f for f in os.listdir(cookie_dir) if f.endswith(".txt")]
    if not cookies_files:
        return None
    return os.path.join(cookie_dir, random.choice(cookies_files))


def time_to_seconds(time_str):
    """Convert time string (MM:SS) to seconds"""
    try:
        if ':' in time_str:
            minutes, seconds = map(int, time_str.split(':'))
            return minutes * 60 + seconds
        return int(time_str)
    except:
        return 0


async def download_song(link: str):
    video_id = link.split('v=')[-1].split('&')[0]
    download_folder = "downloads"

    # Check if file already exists
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
                        print(f"Downloading from API: {download_url}")
                        return await download_file(session, download_url, video_id, data)
                else:
                    print(f"NEW_API failed with status: {response.status}")
        except Exception as e:
            print(f"NEW_API exception: {e}")

    print("API method failed, falling back to yt-dlp cookies method")
    return None


async def download_file(session, download_url, video_id, data):
    try:
        file_format = data.get("format", "mp3")
        file_extension = file_format.lower()
        file_name = f"{video_id}.{file_extension}"
        download_folder = "downloads"
        os.makedirs(download_folder, exist_ok=True)
        file_path = os.path.join(download_folder, file_name)

        async with session.get(download_url) as response:
            with open(file_path, 'wb') as f:
                while True:
                    chunk = await response.content.read(8192)
                    if not chunk:
                        break
                    f.write(chunk)
        print(f"Successfully downloaded: {file_path}")
        return file_path
    except Exception as e:
        print(f"Download error: {e}")
        return None


async def check_file_size(link):
    cookie_file = cookie_txt_file()
    if not cookie_file:
        print("No cookie file found")
        return None
        
    async def get_format_info(link):
        proc = await asyncio.create_subprocess_exec(
            "yt-dlp", "--cookies", cookie_file, "-J", link,
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

    async def url(self, message_1=None) -> Union[str, None]:
        # Simplified URL extraction - you can modify this as needed
        return None

    async def details(self, link: str, videoid: Union[bool, str] = None):
        if videoid:
            link = self.base + link
        if "&" in link:
            link = link.split("&")[0]
        
        # Extract video ID from link
        video_id = link.split('v=')[-1].split('&')[0]
        
        # Return basic info without external API calls
        return f"Video {video_id}", "0:00", 0, f"https://img.youtube.com/vi/{video_id}/default.jpg", video_id

    async def download(
        self, link: str, mystic=None,
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
            cookie_file = cookie_txt_file()
            if not cookie_file:
                print("No cookie file found for fallback download")
                return None
                
            opts = {
                "format": "bestaudio/best",
                "outtmpl": "downloads/%(id)s.%(ext)s",
                "geo_bypass": True,
                "nocheckcertificate": True,
                "quiet": True,
                "cookiefile": cookie_file,
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
            cookie_file = cookie_txt_file()
            if not cookie_file:
                print("No cookie file found for fallback download")
                return None
                
            opts = {
                "format": "(bestvideo[height<=?720][ext=mp4])+bestaudio[ext=m4a]",
                "outtmpl": "downloads/%(id)s.%(ext)s",
                "geo_bypass": True,
                "nocheckcertificate": True,
                "quiet": True,
                "cookiefile": cookie_file,
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
            print("API download failed, trying yt-dlp fallback...")
            return await loop.run_in_executor(None, audio_dl)

        elif video:
            # Simplified video download without size check
            return await loop.run_in_executor(None, video_dl)
        else:
            downloaded_file = await download_song(link)
            if downloaded_file:
                return downloaded_file
            print("API download failed, trying yt-dlp fallback...")
            return await loop.run_in_executor(None, audio_dl)


# Example usage function
async def main():
    # Example YouTube URL
    youtube_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    
    # Create API instance
    api = YouTubeAPI()
    
    # Check if URL exists
    if await api.exists(youtube_url):
        print("URL is valid")
        
        # Get video details
        title, duration_min, duration_sec, thumbnail, vidid = await api.details(youtube_url)
        print(f"Title: {title}")
        print(f"Duration: {duration_min}")
        print(f"Thumbnail: {thumbnail}")
        print(f"Video ID: {vidid}")
        
        # Download audio
        print("Downloading audio...")
        result = await api.download(youtube_url, None, songaudio=True)
        if result:
            print(f"Download successful: {result}")
        else:
            print("Download failed")
    else:
        print("Invalid YouTube URL")


if __name__ == "__main__":
    asyncio.run(main())
