import os
import asyncio
import shutil
from dotenv import load_dotenv
import aiohttp
import aiofiles
import uptobox

load_dotenv()
dl_path = os.getenv('dl_path')
dl_path = os.environ.get('DL_PATH')

async def save(client, sname, title, cdata): # pylint: disable=too-many-arguments
    cpath = f'{dl_path}/{sname}/{title}'
    os.makedirs(cpath, exist_ok=True)
    server = cdata['sAtsServerUrl']

    for d in cdata['files']:
        full_url = f'{server}{d["secureUrl"]}'
        if '.jpeg&gid' in full_url or '.jpg&gid' in full_url:
            fname = f'{d["no"]:03d}.jpeg' #1. leading zero
        elif '.png&gid' in full_url:
            fname = f'{d["no"]:03d}.png' #1. leading zero


        print(f'Downloading {fname}...')

        async with aiofiles.open(f'{cpath}/{fname}', 'wb') as f:
            async with client.get(full_url) as r:

                await f.write(await r.read())
        print(f'{fname} Downloaded!\n')
        await asyncio.sleep(0)

    lpath = f'{dl_path}/{sname}'
    zres = zpr(dest=lpath, cname=title, to_zip=cpath)
    if zres == 'succes':
        link = uptobox.upload(site='kkp', stitle=sname,ctitle=title,
                local_path=f'{lpath}/zipped/{title}.zip')
        os.rmdir(lpath)
        return link
    return 'failed to zip'

async def get_sdetail(ctx, sname, sdata):
    try:
        link = uptobox.get_link('kkp', sname)
        slink = f', Folder link : {link}'
    except Exception as e: # pylint: disable= broad-except
        print(e)
        slink = ''
    await ctx.reply(f'Series id & Title: {sname}, Total Chapter: {sdata["total_count"]}{slink}')

async def main(ctx, serid, chlist):

    async with aiohttp.ClientSession() as client:
        status, sname, sdata = await series_data(client, serid)
        if status != 200:

            await ctx.reply(f'Failed to parse the server series_data it return  {status}')
            return status

        sname = f'{serid} - {sname}'
        if chlist is None:
            return await get_sdetail(ctx, sname, sdata)
        chlist = chan_gen(chlist)
        return await get_it(client, ctx, sdata, sname, chlist)

async def get_it(client, ctx, sdata, sname, chlist):

    for d in sdata['singles']:

        no = d['order_value']
        if no not in chlist:
            continue

        on_dbx = uptobox.check_files(site='kkp', stitle=sname)
        # pid = d['id']
        title = f'{no:03d} - {d["title"]}' #1. leading zero
        if f'{title}.zip' in on_dbx:
            await ctx.reply(uptobox.get_link(site='kkp',
                stitle=sname,ctitle=title))
            continue

        gstatus, cdata = await gdata(client, d['id'])
        print(cdata)
        if gstatus != 200:
            await ctx.reply(f'Failed to get chapter data. it return {gstatus}')
            continue

        try:
            result = await save(client=client,
                    sname=sname, title=title,
                    cdata=cdata['downloadData']['members'])
        except KeyError as ke:
            await ctx.reply(f'''this chapter may be unavailable or inside paywall: {no}
                    {cdata["message"]}''')
            print(ke)
            break
        print(result)
        await ctx.reply(result)

        #print(f'title: {title}\nno: {no}\npid: {pid}\n')
        await asyncio.sleep(0)
        # ctx.reply(result)
    #pass

async def gdata(client,prodid):
    url = 'https://api2-page.kakao.com/api/v1/inven/get_download_data/web'
    data = {
            'productId': prodid,
            'device_mgr_uid': 'Linux - Firefox',
            'device_model': 'Linux - Firefox',
            'deviceId': '7a4ed7b1b641da9effc24cfb99d61fdd'
            }
    async with client.post(url, data=data) as r:
        # assert r.status == 200
        status = r.status
        return status, await r.json() # ['downloadData']['members']


async def series_data(client, serid):
    url = 'https://api2-page.kakao.com/api/v5/store/singles'
    data = {
            'seriesid': serid,
            'page':0,
            'direction': 'asc',
            'page_size': 100,
            'without_hidden': 'true'
            }
    async with client.post(url, data=data) as r:
        status = r.status
        sdata = await r.json()
        try:
            sname = sdata['singles'][0]['title'].strip(' 1화')
        except IndexError as ie:
            print(ie)
            print(sdata)
        return status, sname, sdata # ['singles']

def zpr(dest, cname, to_zip):
    base_name = f'{dest}/zipped/{cname}'
    if not os.path.isfile(f'{base_name}.zip'):
        try:
            shutil.make_archive(base_name, 'zip', to_zip)

        except Exception as e: # pylint: disable= broad-except
            print(e)
            return f'i messed up \n {e}'
    return 'succes'

def chan_gen(strnum):
    """ Generate chapter number from format 1,3-4,6
    or something like that
    :return: list of number [1,3,4,6]
    """

    if "," in strnum:
        a = strnum.split(',')
    else:
        a = [strnum]

    result = []
    for x in a:
        if '-' in x:
            xr = x.split('-')
            for b in range(int(xr[0]), int(xr[1])+1):
                result.append(b)
            continue
        result.append(int(x))
    return result




if __name__ == '__main__':

    seriesid = 56310553
    to_get = [1,]
    loop = asyncio.get_event_loop()
    print(loop.run_until_complete(main(seriesid, to_get, None)))

#foot_note :
#1. leading zero = https://stackoverflow.com/questions/134934/display-number-with-leading-zeros
