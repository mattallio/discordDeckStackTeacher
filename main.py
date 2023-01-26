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

    if message.author == client.user:
        return

    if "/memorandum" in message.content:
        stack = card2numbers.Memorandum
        await trainStack(message, stack)

    if "/mnemonica" in message.content:
        stack = card2numbers.Mnemonica
        await trainStack(message, stack)

    if "/redford" in message.content:
        stack = card2numbers.Redford
        await trainStack(message, stack)

    if "/aronson" in message.content:
        stack = card2numbers.Aronson
        await trainStack(message, stack)

    if "/train" in message.content:
        if message.channel.name == "memorandum":
            stack = card2numbers.Memorandum
        elif message.channel.name == "mnemonica":
            stack = card2numbers.Mnemonica
        elif message.channel.name == "redford-stack":
            stack = card2numbers.Redford
        elif message.channel.name == "aronson-stack":
            stack = card2numbers.Aronson
        else:
            return
        await trainStack(message, stack)

if __name__ == "__main__":
    with open("token.txt", "r") as f:
        TOKEN = f.read()
    try:
        keep_alive()
        client.run(TOKEN)
    except discord.errors.HTTPException:
        print("\n\n\nBLOCKED BY RATE LIMITS\nRESTARTING NOW\n\n\n")
        os.system("python3 restarter.py")
        os.system('kill 1')