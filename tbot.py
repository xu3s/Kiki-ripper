import os
import asyncio
#from dotenv import load_dotenv
from discord.ext import commands
import discord
import ccrawler

#load_dotenv()
#TOKEN = os.getenv('DISCORD_TOKEN')
TOKEN = os.environ.get('DISCORD_TOKEN')
bot = commands.Bot(command_prefix='!g')


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.command('hei')
async def hei(ctx):
    response = f"Oh hai {ctx.message.author.mention}"
    await ctx.reply(response,
            mention_author=True,
            #file=discord.File(r'/data/data/com.termux/files/home/sel.py'),
            embed=discord.Embed(title="test embed",
                url="https://manga.bilibili.com/detail/mc29562?from=manga_index",
                description="this the descrription"))

@bot.command('get')
async def get(ctx, link, chanum=None):
    await ctx.send('please be patient, as it downloading in the background')
    # loop = asyncio._get_running_loop()
    if chanum is not None:
        n = ccrawler.chan_gen(chanum)
        for a in n:
            result = ccrawler.mdownload(link, a)
            def itrt():
                return '\n'.join(x for x in result)
            r2 = itrt()
            await ctx.reply(r2)
    else:
        result = ccrawler.mdownload(link, chanum)
        def itrt():
            return '\n'.join(x for x in result)
        # r2 = await loop.run_in_executor(None, itrt)
        r2 = itrt()
        await ctx.reply(r2)
    await ctx.send('Done!')

@bot.command('site')
async def site(ctx):
    content = ['163.bilibili.com', '99.hhxxee.com', 'ac.qq.com', 'beta.sankakucomplex.com', 'chan.sankakucomplex.com', 'comic.acgn.cc', 'comic.sfacg.com', 'comicbus.com', 'danbooru.donmai.us', 'deviantart.com', 'e-hentai.org', 'exhentai.org', 'gelbooru.com', 'hk.dm5.com', 'ikanman.com', 'imgbox.com', 'konachan.com', 'm.dmzj.com', 'm.manhuabei.com', 'm.wuyouhui.net', 'manga.bilibili.com', 'manhua.dmzj.com', 'manhuagui.com', 'nijie.info', 'pixabay.com', 'raw.senmanga.com', 'seemh.com', 'seiga.nicovideo.jp', 'smp.yoedge.com', 'tel.dm5.com', 'tsundora.com', 'tuchong.com', 'tumblr.com', 'tw.weibo.com', 'wix.com', 'www.177pic.info', 'www.1manhua.net', 'www.33am.cn', 'www.36rm.cn', 'www.8comic.com', 'www.99comic.com', 'www.aacomic.com', 'www.artstation.com', 'www.buka.cn', 'www.cartoonmad.com', 'www.chuixue.com', 'www.chuixue.net', 'www.cocomanhua.com', 'www.comicvip.com', 'www.dm5.com', 'www.dmzj.com', 'www.facebook.com', 'www.flickr.com', 'www.gufengmh.com', 'www.gufengmh8.com', 'www.hhcomic.cc', 'www.hheess.com', 'www.hhmmoo.com', 'www.hhssee.com', 'www.hhxiee.com', 'www.iibq.com', 'www.manhuadui.com', 'www.manhuaren.com', 'www.mh160.com', 'www.ohmanhua.com', 'www.pixiv.net', 'www.setnmh.com', 'www.tohomh.com', 'www.tohomh123.com', 'www.xznj120.com', 'yande.re'] # pylint: disable=line-too-long
    contents = [content[x:x+10] for x in range(0, len(content),10)]
    pages = len(contents)
    cur_page = 1
    nl = '\n'
    message = await ctx.reply(embed=discord.Embed(title="Supported Site:",
        description=f"Page {cur_page}/{pages}:\n{nl.join(contents[cur_page-1])}"))
    # getting the message object for editing and reacting

    await message.add_reaction("◀️")
    await message.add_reaction("▶️")

    def check(reaction, user):
        return user == ctx.author and str(reaction.emoji) in ["◀️", "▶️"]
        # This makes sure nobody except the command sender can interact with the "menu"

    while True:
        try:
            reaction, user = await bot.wait_for("reaction_add", timeout=15, check=check)
            # waiting for a reaction to be added - times out after x seconds, 60 in this
            # example

            if str(reaction.emoji) == "▶️" and cur_page != pages:
                cur_page += 1
                await message.edit(embed=discord.Embed(title="Supported Site:",
                    description=f"Page {cur_page}/{pages}:\n{nl.join(contents[cur_page-1])}"))
                # await message.edit(content=f"Page {cur_page}/{pages}:\n{nl.join(contents[cur_page-1])}")
                await message.remove_reaction(reaction, user)

            elif str(reaction.emoji) == "◀️" and cur_page > 1:
                cur_page -= 1
                await message.edit(embed=discord.Embed(title="Supported Site:",
                        description=f"Page {cur_page}/{pages}:\n{nl.join(contents[cur_page-1])}"))
                # await message.edit(content=f"Page {cur_page}/{pages}:\n{nl.join(contents[cur_page-1])}")
                await message.remove_reaction(reaction, user)

            else:
                await message.remove_reaction(reaction, user)
                # removes reactions if the user tries to go forward on the last page or
                # backwards on the first page
        except asyncio.TimeoutError:
            await message.delete()
            break
            # ending the loop if user doesn't react after x seconds


    # await ctx.reply("supported site:\n"+'\n'.join(a for a in webl))

@bot.command('ping')
async def ping(ctx):
    await ctx.send(f'pong! {bot.latency}')
# async def on_message(message):
    # we do not want the bot to reply to itself
#    if message.author.id == client.user.id:
#        return

#    if message.content.startswith('!hello'):
#        await message.reply('Hello!', mention_author=True)
#    if message.content.startswith('!hei'):
#        await message.reply('Oh hai', mention_author=True)

# client = MyClient()
bot.run(TOKEN)
