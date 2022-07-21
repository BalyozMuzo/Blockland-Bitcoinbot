import discord
from discord.ext import commands
import requests
import json
import asyncio
from numerize import numerize
import config

client = commands.Bot(command_prefix = '$')

async def status_task():

    while True:

        getir = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd&include_market_cap=true&include_24hr_vol=true&include_24hr_change=true&include_last_updated_at=true").text
        getir = json.loads(getir)

        getir_usd = getir["bitcoin"]["usd"]
        getir_mcap = getir["bitcoin"]["usd_market_cap"]
        getir_24 = getir["bitcoin"]["usd_24h_change"]
        getir_24_vol = getir["bitcoin"]["usd_24h_vol"]

        await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"MCAP:{numerize.numerize(getir_mcap)}$"))
        for guild in client.guilds:
            await guild.me.edit(nick=f"BTC : {getir_usd}$ ")

        await asyncio.sleep(6)
        await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"24hChange:%{numerize.numerize(getir_24)}"))
        await asyncio.sleep(6)
        await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"24hVol:{numerize.numerize(getir_24_vol)}"))
        await asyncio.sleep(6)

try :
    @client.event
    async def on_ready():   
        client.loop.create_task(status_task())
        print('blockland Etherbot hazir')

except :
    False

client.run(config.BITCOIN_TOKEN)
