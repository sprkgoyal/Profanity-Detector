import discord
from collections import defaultdict
from discord.ext import commands

count_abuse = defaultdict(lambda : 0)
token = "NzM3OTc5MjA5MTYyNjg2NTQ0.XyFOsg.N8QLCWXI_VCXdjgFlw5yALf94oU"

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
# @commands.has_permissions(administrator = True)
async def add(ctx, *, word):
    global abuse
    if word not in abuse:
        abuse.add(word.lower())
        abuse_file = open("list.txt", "a")
        abuse_file.write(f"{word.lower()}\n")
        abuse_file.close()
    await ctx.send("Added a abuse in the Dictionary")

@client.command()
# @commands.has_permissions(administrator = True)
async def remove(ctx, *, word):
    global abuse
    abuse.remove(word.lower())
    await ctx.send("Removed a abuse from the Dictionary")
    abuse_file = open("list.txt", "w")
    for word in abuse:
        abuse_file.write(f"{word}\n")
    abuse_file.close()

@client.event
async def on_message(message : discord.Message):
    if message.author == client.user:
        return

    if message.content.startswith(".add") or message.content.startswith(".remove"):
        if "admin" in [mem.name.lower() for mem in message.author.roles]:
            await client.process_commands(message)
        else:
            await message.channel.send("Only Admins can use this command")
        return

    if message.content == ".help":
        await message.channel.send("""Hello there, and welcome to the help section of Abuse Detector

There are only two commands available here and each command starts with '.' also called period
1) add abusive_word, this adds abusive_word in the abuse dictionary for future detection
2) remove word, this removes a word from the abuse dictionary""")
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
            await message.channel.send(f"{message.author}, your message contains abusive word(s)")
            count_abuse[message.author] += 1
            if count_abuse[message.author] == 1:
                await message.channel.send(f"This is your first warning, if you abuse two more times then you will be kicked from this channel")
            elif count_abuse[message.author] == 2:
                await message.channel.send(f"This is your second warning, if you abuse one more time then you will be kicked from this channel")
            else:
                await message.channel.send(f"That's it, you crossed the limit so you are kicked from the server")
                try:
                    await message.channel.guild.kick(message.author, reason = "Using Abusive Language")
                except:
                    await message.channel.send("I can't kick you right now, but you will be kicked shortly...")
                count_abuse[message.author] = 0
            return

client.run(token)
