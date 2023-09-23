# © BugHunterCodeLabs ™
# © bughunter0 / nuhman_pk
# 2021
# Copyright - https://en.m.wikipedia.org/wiki/Fair_use

import os 
from os import error
import speedtest   
import logging
import pyrogram
import math
import requests
from decouple import config
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.types import User, Message

bughunter0 = Client(
    "SpeedTestBot",
    bot_token = os.environ["BOT_TOKEN"],
    api_id = int(os.environ["API_ID"]),
    api_hash = os.environ["API_HASH"]
)

@bughunter0.on_message(filters.command(["start"]))
async def start(bot, update):
 txt = await update.reply_text("ചത്തോന്ന് അറിയാൻ വന്നതാവും ല്ലേ !!")

@bughunter0.on_message(filters.command("speedtest"))
async def run_speedtest(client, message):
    m = await message.reply_text("⚡️ Running Server Speedtest")
    
    try:
        test = speedtest.Speedtest()
        test.get_best_server()
        
        m = await m.edit("⚡️ Running Download Speedtest..")
        download_speed = test.download() / 1024 / 1024  # Convert to Mbps
        
        m = await m.edit("⚡️ Running Upload Speedtest...")
        upload_speed = test.upload() / 1024 / 1024  # Convert to Mbps
        
        test.results.share()
        result = test.results.dict()
    except Exception as e:
        await m.edit(str(e))  # Convert exception to string before editing
        return
    
    m = await m.edit("🔄 Sharing Speedtest Results")
    
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
        response = requests.get(result["share"], headers=headers)
        response.raise_for_status()  # Raise exception for HTTP errors
        content = response.content
        
        path = "speedtest_result.png"  # Provide a local file name
        with open(path, "wb") as file:
            file.write(content)
    except requests.exceptions.RequestException as req_err:
        await m.edit(f"Error downloading: {req_err}")
        return
    
    output = f"""💡 <b>SpeedTest Results</b>
<u><b>Client:</b></u>
<b>ISP:</b> {result['client']['isp']}
<b>Country:</b> {result['client']['country']}
<u><b>Server:</b></u>
<b>Name:</b> {result['server']['name']}
<b>Country:</b> {result['server']['country']}, {result['server']['cc']}
<b>Sponsor:</b> {result['server']['sponsor']}
⚡️ <b>Ping:</b> {result['ping']}
🚀 <b>Download Speed:</b> {download_speed:.2f} Mbps
🚀 <b>Upload Speed:</b> {upload_speed:.2f} Mbps"""

    msg = await client.send_photo(
        chat_id=message.chat.id, photo=path, caption=output, parse_mode="html"
    )
    os.remove(path)
    await m.delete()
bughunter0.run()
