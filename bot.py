import discord
from collections import defaultdict
from discord.ext import commands

count_abuse = defaultdict(lambda : 0)

client = commands.Bot(command_prefix = '.')
abuse = set(['fuck', 'fucking', 'fucked', 'chut', 'chuchi', 'loda', 'lode', 'madarchod', 
         'bitch', 'fucker', 'motherfucker', 'sisterfucker', 'dick', 'vagina', 'tit',
         'tits', 'ass', 'asshole', 'cunt', 'mallu', 'boobs', 'boob', 'bbc', 'orgasm', 
         'kutta', 'kamina', 'kutiya', 'behenchod', 'bhenchod', 'benchod', 'chod', 'chudai', 'butt', 'buttocks',
         'prostitute', 'chuda', 'chud', 'chudi', 'bc', 'mc', 'lund'])

@client.event
async def on_ready():
    print("Bot is Deployed.")

@client.event
async def on_message(message : discord.Message):
    if message.author == client.user:
        return

    words = message.content.split()

    for word in words:
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
                    await message.channel.send("You have powers so you are safe else ...")
                count_abuse[message.author] = 0
            break

client.run("NzM3OTc5MjA5MTYyNjg2NTQ0.XyFOsg.N8QLCWXI_VCXdjgFlw5yALf94oU")