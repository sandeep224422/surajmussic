
    ─「 ᴅᴇᴩʟᴏʏ ᴏɴ ʜᴇʀᴏᴋᴜ 」─
</h3>
<img src="https://user-images.githubusercontent.com/73097560/115834477-dbab4500-a447-11eb-908a-139a6edaec5c.gif">
<p align="center"><a href="https://dashboard.heroku.com/new?template=https://github.com/Suraj08832/sonammusic"> <img src="https://img.shields.io/badge/Deploy%20On%20Heroku-00FFFF?style=for-the-badge&logo=heroku" width="220" height="38.45"/></a></p>
<img src="https://user-images.githubusercontent.com/73097560/115834477-dbab4500-a447-11eb-908a-139a6edaec5c.gif">

## 🎵 API Configuration

The bot uses a dual-API system for YouTube song downloads:

- **Primary API**: `NEW_API_URL` for first attempt at song downloads
- **Fallback API**: `API_URL` and `API_KEY` for when the primary API fails
- **Cookies Fallback**: If both APIs fail, the bot automatically falls back to using yt-dlp with cookies

### Environment Variables

```env
# YouTube Song Download APIs
API_URL=https://api.thequickearn.xyz
API_KEY=NxGBNexGenBotsad3e6e
NEW_API_URL=https://apikeyy-zeta.vercel.app/api
```

The bot will automatically try the new API first, then the main API if it fails, and finally use cookies if both APIs fail.
