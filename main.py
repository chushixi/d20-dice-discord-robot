import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os
import random
import asyncio
import edge_tts
from discord import FFmpegPCMAudio

load_dotenv()
token = os.getenv("DISCORD_TOKEN")

handlers = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.voice_states = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

    for command in bot.commands:
        print(f"🛠️ {command.name}")

@bot.command()
#!NoFIGHT
async def nofight(ctx, user1: discord.Member, user2: discord.Member):
    roll1 = random.randint(1, 20)
    roll2 = random.randint(1, 20)

    if roll1 > roll2:
        await ctx.send(f'{user1.mention} : {roll1} vs {user2.mention} : {roll2} \n🎉 {user1.display_name} wins!')
    elif roll1 < roll2:
        await ctx.send(f'{user1.mention} : {roll1} vs {user2.mention} : {roll2} \n🎉 {user2.display_name} wins!')
    else:
        await ctx.send(f'{user1.mention} : {roll1} vs {user2.mention} : {roll2} \n🎉 It is a tie!')
        
@bot.command()
async def bing(ctx):
    await ctx.send("bong!")


@bot.command()
async def join(ctx):
    if ctx.author.voice and ctx.author.voice.channel:
        vc_channel = ctx.author.voice.channel
        voice_client = await vc_channel.connect()
        await ctx.send(f"已經加入語音頻道：{vc_channel.name}")
    else:
        await ctx.send("⚠️ 你不在語音頻道，我不能加入喔！")

@bot.command()
async def helpwe(ctx, user1: discord.Member, user2: discord.Member):
    
    if ctx.voice_client is None:
        await ctx.send("❌ 我還沒加入任何語音頻道，請先 `!join`")
    elif ctx.author.voice is None:
        await ctx.send("❌ 你沒有在語音頻道中")
    elif ctx.voice_client.channel != ctx.author.voice.channel:
        await ctx.send("⚠️ 你跟我不在同一個語音頻道喔，請先進來我的頻道")
    else:# 進入播放語音的邏輯
        await ctx.send("🔍 helpWE 指令開始執行")
        roll1 = random.randint(1, 20)
        roll2 = random.randint(1, 20)

        if roll1 > roll2:
            result = (f'{user1.display_name} 比數為 {roll1} 對到 {user2.display_name} 比數為 {roll2} 🎉🎉🎉 {user1.display_name} 獲勝!{user2.display_name}滾一邊去!')
        elif roll1 < roll2:
            result = (f'{user1.display_name} 比數為 {roll1} 對到 {user2.display_name} 比數為 {roll2} 🎉🎉🎉 {user2.display_name} 獲勝!{user1.display_name}滾一邊去!')
        else:
            result = (f'{user1.display_name} 比數為 {roll1} 對到 {user2.display_name} 比數為 {roll2} 🎉🎉🎉 你們別吵了兩邊平手!')

        output_file = "output.mp3"
        communicate = edge_tts.Communicate(text=result, voice="zh-TW-HsiaoYuNeural")
        await communicate.save(output_file)
    
        audio = FFmpegPCMAudio(output_file)
        ctx.voice_client.play(audio)
    
        while ctx.voice_client.is_playing():
            await asyncio.sleep(1)

        await ctx.voice_client.disconnect()
        os.remove(output_file)


@bot.command()
async def quit(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send("已經離開語音頻道！")
    else:
        await ctx.send("我不在語音頻道中！")




bot.run(token, log_handler=handlers, log_level=logging.DEBUG)

