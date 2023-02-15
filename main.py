import discord
import random
import time
import os
#import schedule
import pandas as pd
from threading import Thread
from keep_alive import keep_alive

intents=discord.Intents.default()
intents.message_content = True
#intents.members = True

client = discord.Client(intents=intents)

card2numbers = pd.read_excel("0-card-to-number.xlsx")

recents = {}

@client.event
async def on_ready():
    print(f"Logged in as {client.user}")

async def trainStack(message, stack):
    card = random.randint(1,52)
    photo = open(fr"Cards/{card}.jpg", "rb")
    await message.channel.send(file=discord.File(photo))
    photo.close()
    number = int(stack[card-1])
    if number != 0:
        time.sleep(5)
    await message.channel.send(number)

@client.event
async def on_message(message):
    #print(message)
    #print(message.type.value)
    if message.reference != None:
        print(message.reference)
    #print(message.type)
    if message.reference != None and message.reference.message_id in recents[message.channel.id]:
        print("noice")

    if message.author == client.user:
        if message.channel.id in recents and len(recents[message.channel.id]) == 5:
            recents[message.channel.id].pop(0)
        if message.channel.id not in recents:
            recents[message.channel.id] = []
        recents[message.channel.id].append(message.id)
        print(recents)
        return

    if ".memorandum" in message.content:
        stack = card2numbers.Memorandum
        await trainStack(message, stack)

    if ".mnemonica" in message.content:
        stack = card2numbers.Mnemonica
        await trainStack(message, stack)

    if ".daortiz" in message.content:
        stack = card2numbers.Daortiz
        await trainStack(message, stack)

    if ".redford" in message.content:
        stack = card2numbers.Redford
        await trainStack(message, stack)

    if ".aronson" in message.content:
        stack = card2numbers.Aronson
        await trainStack(message, stack)

    if ".t" in message.content:
        if message.channel.name == "memorandum-stack":
            stack = card2numbers.Memorandum
        elif message.channel.name == "mnemonica-stack":
            stack = card2numbers.Mnemonica
        elif message.channel.name == "daortiz-stack":
            stack = card2numbers.Daortiz
        elif message.channel.name == "redford-stack":
            stack = card2numbers.Redford
        elif message.channel.name == "aronson-stack":
            stack = card2numbers.Aronson
        else:
            return
        await trainStack(message, stack)

    if ".help" in message.content:
        helpMessage = open(r"help.txt", "r")
        await message.channel.send(helpMessage.read())
        helpMessage.close()

if __name__ == "__main__":
    with open("token.txt", "r") as f:
        TOKEN = f.read()
    #TOKEN = os.environ["TOKEN"]
    #keep_alive()
    client.run(TOKEN)