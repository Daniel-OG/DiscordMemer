from typeform import Typeform
import discord
import os
import random
import requests

DISCORD_TOKEN = open('DISCORD_TOKEN', 'r').read().replace('\n', '')
TYPEFORM_TOKEN = open('TYPEFORM_TOKEN', 'r').read().replace('\n', '')

typeform = Typeform(TYPEFORM_TOKEN)

client = discord.Client()


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$joke'):

        jokes = typeform.responses.list("v15AHAUD").get("items")
        result = random.choice(jokes).get("answers")[0].get("text")

        await message.channel.send(str(result), tts=True)

    elif message.content.startswith('$meme'):

        memes = typeform.responses.list("hTIEdVLY").get("items")
        result = random.choice(memes).get("answers")[0].get("file_url")

        headers_dict = {"Authorization" : "Bearer " + TYPEFORM_TOKEN}
        r = requests.get(result, headers=headers_dict, allow_redirects=True)
        open("file.jpg", "wb").write(r.content)

        await message.channel.send(file=discord.File("file.jpg"))

client.run(DISCORD_TOKEN)

