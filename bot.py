import discord
import os
from collections import defaultdict
from datetime import datetime, timedelta
from discord.ext import commands
from math import ceil, floor

token = os.environ["BOT_TOKEN"]
time_limit = 60
change_time = datetime.now()
count_abuse = defaultdict(lambda : [0, datetime.now(), time_limit])

client = commands.Bot(command_prefix = '.')
abuse = set()
abuse_file = open("list.txt", "r")
for word in abuse_file:
    abuse.add(word.replace("\n", ""))

needed = set()
for i in "qwertyuiopasdfghjklzxcvbnm0123456789":
    needed.add(i)
    needed.add(i.upper())

@client.event
async def on_ready():
    print("Bot is Deployed.")

@client.command()
async def add(ctx, *, word):
    global abuse
    if word not in abuse:
        abuse.add(word.lower())
        abuse_file = open("list.txt", "a")
        abuse_file.write(f"{word.lower()}\n")
        abuse_file.close()
    await ctx.send("Added a abuse in the Dictionary")

@client.command()
async def remove(ctx, *, word):
    global abuse
    abuse.remove(word.lower())
    await ctx.send("Removed a abuse from the Dictionary")
    abuse_file = open("list.txt", "w")
    for word in abuse:
        abuse_file.write(f"{word}\n")
    abuse_file.close()

@client.command()
async def set(ctx, *, minutes):
    global time_limit, change_time
    time_limit = int(minutes)
    change_time = datetime.now()
    await ctx.send(f"Time Limit has been changed to {minutes} minutes")


@client.event
async def on_message(message : discord.Message):
    global time_limit
    if message.author == client.user:
        return

    if message.content.startswith(".add") or message.content.startswith(".remove") or message.content.startswith(".set"):
        if "admin" in [mem.name.lower() for mem in message.author.roles]:
            await client.process_commands(message)
        else:
            await message.channel.send("Only Admins can use this command")
        return

    if message.content == ".remaining":
        cur = datetime.now()
        prev = count_abuse[message.author][1]
        if cur - prev > timedelta(minutes=time_limit):
            count_abuse[message.author][1] = change_time
            prev = change_time
        lim = min(count_abuse[message.author][2], time_limit)
        count_abuse[message.author][2] = lim
        if cur-prev < timedelta(minutes=lim) and count_abuse[message.author][0] > 0:
            await message.channel.send(f"@{message.author} has to wait **{floor(lim - (cur - prev).total_seconds()/60)} Minutes and {ceil(60 - (cur - prev).total_seconds()%60)%60} Seconds** until your count resets")
        else:
            count_abuse[message.author][0] = 0
            await message.channel.send("You are free to go man")
        return

    if message.content == ".help":
        await message.channel.send("""Hello there, and welcome to the help section of Abuse Detector

There are only four commands available here and each command starts with '.' also called period
1) add abusive_word, this adds abusive_word in the abuse dictionary for future detection
2) remove word, this removes a word from the abuse dictionary
3) set minutes, sets the count of abuses to zero after 'minutes' minutes from his/her last abuse
4) remaining, tells us how much time is left until your count resets""")
        return

    words = message.content.split()
    new_words = []
    for word in words:
        rem = ""
        for ch in word:
            if ch not in needed:
                rem += ch
        word = word.strip(rem)
        new_words.append(word)

    for word in new_words:
        if word.lower() in abuse:
            cur = datetime.now()
            if cur - count_abuse[message.author][1] >= timedelta(minutes=time_limit):
                count_abuse[message.author][0] = 0
            count_abuse[message.author][1] = datetime.now()
            count_abuse[message.author][2] = time_limit
            count_abuse[message.author][0] += 1
            await message.channel.send(f"@{message.author}, your message contains abusive word(s)")
            if count_abuse[message.author][0] == 1:
                await message.channel.send(f"This is your **first** warning, if you abuse two more times then you will be kicked from this channel")
            elif count_abuse[message.author][0] == 2:
                await message.channel.send(f"This is your **second** warning, if you abuse one more time then you will be kicked from this channel")
            else:
                await message.channel.send(f"That's it, you crossed the limit so you are kicked from the server")
                try:
                    await message.channel.guild.kick(message.author, reason = "Using Abusive Language")
                except:
                    await message.channel.send("I can't kick you right now, but you will be kicked shortly...")
                count_abuse[message.author][0] = 0
            return

client.run(token)
