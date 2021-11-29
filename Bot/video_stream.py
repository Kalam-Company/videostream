import re 
import os
from pytgcalls import GroupCallFactory
from pyrogram import Client, filters
from pyrogram.types import Message
# from py_youtube import ytdl
from py_youtube import ytdl 

API_ID = os.environ.get("API_ID",12345)
API_HASH = os.environ.get("API_HASH","")
SESSION_NAME = os.environ.get("SESSION_NAME","")
CHAT = os.environ.get("CHAT","")
ADMIN = int(os.environ.get("ADMIN", 923943045))

app = Client(SESSION_NAME, API_ID, API_HASH)

group_call_factory = GroupCallFactory(app, GroupCallFactory.MTPROTO_CLIENT_TYPE.PYROGRAM)
VIDEO_CALL = {}

@Client.on_message(filters.private & filters.user(ADMIN) & filters.command(["start"]))
async def start(client, m: Message):
	await m.reply("வணக்கம், \n\t\t I am a Live Streamer...! 😇 \n I can Stream Video or Audio in your Channel or Group... 🥳\n\n /help to know more... \n\n**©Developed by \n 🔥 @KiruthiVarma.**")

@Client.on_message(filters.private & filters.user(ADMIN) & filters.command(["help"]))
async def help(client, m: Message):
	await m.reply("\n\t\t🪄 **Follow these steps...** 🎺\n\n**For Channels:-**\n\n1. Start Live Stream in your channel. \n\n2. Send me a Direct Download link or YouTube link or TG File and Reply to the message as /play... 🥳 \n\n3. To Stop Streaming Use /stop... 🤙 \n\n**For Groups:-**\n\n1. Start Voice Chat in your group. \n\n2. Send me a Direct Download link or YouTube link or TG File and Reply to the message as /stream... 🥳 \n\n3. To Stop Streaming Use /stopstream... \n\n**©Developed by \n 🔥 @KiruthiVarma.**")

@Client.on_message(filters.private & filters.user(ADMIN) & filters.command(["play"]))
async def play(client, m: Message):
	if (m.reply_to_message):
			link = m.reply_to_message.text
			youtube_regex = r"^(https?\:\/\/)?(www\.youtube\.com|youtu\.?be)\/.+"
			youtube_regex_match = re.match(youtube_regex, link)
			if youtube_regex_match:
				             try:
				             	video_url = ytdl(link).besturl()
				             except Exception as e:
				             	await m.reply(f"**Error** -- `{e}`")
				             	return
				             try:
				             	group_call = group_call_factory.get_group_call()
				             	await group_call.join(CHAT)
				             	await group_call.start_video(video_url,enable_experimental_lip_sync=True)
				             	VIDEO_CALL[CHAT] = group_call
				             	await m.reply("**Started  Streaming!!!** \n\n🚫 /stop to Stop Streaming...")
				             except Exception as e:
				             	await m.reply(f"**Error** -- `{e}`")
				             	
					
			else:
			         	try:
			         		group_call = group_call_factory.get_group_call()
			         		await group_call.join(CHAT)
			         		await group_call.start_video(link,enable_experimental_lip_sync=True)
			         		VIDEO_CALL[CHAT] = group_call
			         		await m.reply("**Started  Streaming!!!** \n\n🚫 /stop to Stop Streaming...")
			         	except Exception as e:
			         	    	await m.reply(f"**Error** -- `{e}`")
				             	
@Client.on_message(filters.private & filters.user(ADMIN) & filters.command(["livestream"]))
async def livestream(client, m: Message):
	if (m.reply_to_message):
			link = m.reply_to_message.text
			youtube_regex = r"^(https?\:\/\/)?(www\.youtube\.com|youtu\.?be)\/.+"
			youtube_regex_match = re.match(youtube_regex, link)
			if youtube_regex_match:
				             try:
				             	video_url = ytdl(link).besturl()
				             except Exception as e:
				             	await m.reply(f"**Error** -- `{e}`")
				             	return
				             try:
				             	group_call = group_call_factory.get_group_call()
				             	await group_call.join(CHAT)
				             	await group_call.start_video(video_url,enable_experimental_lip_sync=False)
				             	VIDEO_CALL[CHAT] = group_call
				             	await m.reply("**Started  Streaming!!!** \n\n🚫 /stop to Stop Streaming...")
				             except Exception as e:
				             	await m.reply(f"**Error** -- `{e}`")
				             	
					
			else:
			         	try:
			         		group_call = group_call_factory.get_group_call()
			         		await group_call.join(CHAT)
			         		await group_call.start_video(link,enable_experimental_lip_sync=False)
			         		VIDEO_CALL[CHAT] = group_call
			         		await m.reply("**Started Streaming!**")
			         	except Exception as e:
			         	    	await m.reply(f"**Error** -- `{e}`")




@Client.on_message(filters.private & filters.user(ADMIN) & filters.command(["stop"]))
async def stop (client, m: Message):
	try:
	       await VIDEO_CALL[CHAT].stop()
	       await m.reply("**Stopped Streaming!**")
	except Exception as e:
		await m.reply(f"**Error** - `{e}`")
