import discord
from collections import defaultdict
from discord.ext import commands

count_abuse = defaultdict(lambda : 0)

client = commands.Bot(command_prefix = '.')
abuse = set(['fuck', 'fucking', 'fucked', 'chut', 'chuchi', 'loda', 'lode', 'madarchod', 
         'bitch', 'fucker', 'motherfucker', 'sisterfucker', 'dick', 'vagina', 'tit', 'bhosad',
         'tits', 'ass', 'asshole', 'cunt', 'mallu', 'boobs', 'boob', 'bbc', 'orgasm', 
         'kutta', 'kamina', 'kutiya', 'behenchod', 'bhenchod', 'benchod', 'chudai', 'butt', 'buttocks',
         'prostitute', 'chuda', 'chud', 'chudi', 'bc', 'mc', 'lund', 'bhosad', 'bhosda', 'randi', 'bsdk', 
         'randikhana', 'jhaat', 'assholes', 'bhosdiwala', 'bosdiwala', 'bhosdiwale', 'bosdiwale',
         'sex', 'pussy', 'bhosdi', 'randwa', 'chodu', 'betichod', 'porn', 'xvideos', 'chutad', 'tmkc', 'mkb',
         'chutiya', 'chutiye', 'gand', 'randirona', 'piss', 'raand', 'gandu', 'lodu', 'chamar', 'bakrichod',
         'jhatu', 'jhaatu', 'tatte', 'tatta'])

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
    abuse.add(word.lower())
    await ctx.send("Added a abuse in the Dictionary")

@client.command()
async def remove(ctx, *, word):
    global abuse
    abuse.remove(word.lower())
    await ctx.send("Removed a abuse from the Dictionary")

@client.command()
async def ping(ctx):
    await ctx.send("testing")

@client.event
async def on_message(message : discord.Message):
    if message.author == client.user:
        return

    if message.content.startswith(".add") or message.content.startswith(".remove"):
        await client.process_commands(message)
        return

    words = message.content.split()
    new_words = []
    for word in words:
        rem = ""
        for ch in word:
            if ch not in needed:
                rem += ch
        # words.remove(word)
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
                    await message.channel.send("I can't kick you right now, but be aware you will be kicked shortly...")
                count_abuse[message.author] = 0
            return

client.run("NzM3OTc5MjA5MTYyNjg2NTQ0.XyFOsg.N8QLCWXI_VCXdjgFlw5yALf94oU")