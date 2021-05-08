import os
import asyncio
from dotenv import load_dotenv
from discord.ext import commands
import asax

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
bot = commands.Bot(command_prefix='!k')

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('----------')

@bot.command()
async def get(ctx, serid, to_get=None):
    await ctx.send(f'Processing {serid}')
    if 'https://page.kakao.com/home?seriesId=' in serid:
        serid = serid.strip('https://page.kakao.com/home?seriesId=')
    await asyncio.get_event_loop().create_task(asax.main(ctx=ctx, serid=serid, chlist=to_get))

@bot.command()
async def ping(ctx):
    await ctx.reply('pong')

if __name__ == '__main__':
    bot.run(TOKEN)
