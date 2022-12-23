import discord
import asyncio
from dotenv import load_dotenv
import os

tmp_discord_client = None

# start discord client (doit etre deplacer dans api_base)


async def discord_client():
    global tmp_discord_client
    if tmp_discord_client:
        return tmp_discord_client
    intents = discord.Intents.default()
    tmp_discord_client = discord.Client(intents=intents)
    load_dotenv()
    TOKEN = os.getenv("DISCORD_TOKEN")
    await tmp_discord_client.start(TOKEN, reconnect=True)
    await tmp_discord_client.wait_until_ready()
    return tmp_discord_client


async def get_discord_client():
    global tmp_discord_client
    if tmp_discord_client:
        return tmp_discord_client
    tmp_discord_client = await discord_client()
    return await tmp_discord_client


# start discord client (doit etre deplacer dans api_base)
