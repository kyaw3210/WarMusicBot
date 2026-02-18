import os
import yt_dlp
import requests
from pyrogram import Client, filters
from pyrogram.types import Message
from youtube_search import YoutubeSearch
from config import BOT_USERNAME as bn
from driver.filters import command

# Song Download Function
@Client.on_message(command(["song", f"song@{bn}"]))
async def song_download(client, message):
    query = " ".join(message.command[1:])
    if not query:
        return await message.reply("🎧 Please give a song name!")
    
    m = await message.reply("🔎 finding song...")
    ydl_ops = {"format": "bestaudio[ext=m4a]"}
    
    try:
        results = YoutubeSearch(query, max_results=1).to_dict()
        link = f"https://youtube.com{results[0]['url_suffix']}"
        title = results[0]["title"][:40]
        thumbnail = results[0]["thumbnails"][0]
        thumb_name = f"{title}.jpg"
        thumb = requests.get(thumbnail, allow_redirects=True)
        open(thumb_name, "wb").write(thumb.content)
        duration = results[0]["duration"]
    except Exception as e:
        await m.edit("❌ song not found...")
        print(str(e))
        return

    await m.edit("📥 downloading file...")
    try:
        with yt_dlp.YoutubeDL(ydl_ops) as ydl:
            info_dict = ydl.extract_info(link, download=False)
            audio_file = ydl.prepare_filename(info_dict)
            ydl.process_info(info_dict)
        
        rep = f"**🎧 Uploader @{bn}**"
        await m.edit("📤 uploading file...")
        await message.reply_audio(
            audio_file,
            caption=rep,
            thumb=thumb_name,
            duration=int(duration.split(':')[0])*60 + int(duration.split(':')[1]) if ':' in duration else 0
        )
        await m.delete()
    except Exception as e:
        await m.edit("❌ error, wait for bot owner to fix")
        print(str(e))
    
    try:
        if os.path.exists(audio_file):
            os.remove(audio_file)
        if os.path.exists(thumb_name):
            os.remove(thumb_name)
    except Exception:
        pass

# Video Download Function
@Client.on_message(command(["vsong", f"vsong@{bn}", "video", f"video@{bn}"]))
async def vsong(client, message):
    query = " ".join(message.command[1:])
    if not query:
        return await message.reply("🎥 Please give a video name!")

    m = await message.reply("🔎 finding video...")
    try:
        results = YoutubeSearch(query, max_results=1).to_dict()
        link = f"https://youtube.com{results[0]['url_suffix']}"
        title = results[0]["title"][:40]
        thumb_name = f"{title}.jpg"
        thumbnail = results[0]["thumbnails"][0]
        thumb = requests.get(thumbnail, allow_redirects=True)
        open(thumb_name, "wb").write(thumb.content)
    except Exception as e:
        await m.edit("❌ video not found...")
        return

    await m.edit("📥 downloading video...")
    try:
        ydl_opts = {"format": "best"}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(link, download=True)
            video_file = ydl.prepare_filename(info_dict)

        await m.edit("📤 uploading video...")
        await message.reply_video(
            video_file,
            caption=f"🎥 **{title}**\n\n**Uploader @{bn}**",
            thumb=thumb_name
        )
        await m.delete()
    except Exception as e:
        await m.edit(f"❌ error: {str(e)}")

    try:
        if os.path.exists(video_file):
            os.remove(video_file)
        if os.path.exists(thumb_name):
            os.remove(thumb_name)
    except Exception:
      
        pass
