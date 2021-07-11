import os
import re
import shutil
import uptobox2
from comiccrawler.mission import Mission
from comiccrawler.analyzer import Analyzer
from comiccrawler.crawler import download

# m = Mission(url="https://manga.bilibili.com/detail/mc29562?from=manga_index")
# Analyzer(m).analyze()
# savepath = "/data/data/com.termux/files/home/developing/discord/saved"
#savepath = "/home/exel/rawbot/saved"
savepath = os.environ.get('DL_PATH')


def mdownload(url,chan=None):
    try:
        m = Mission(url=url)
        Analyzer(m).analyze()
    except Exception as e: #pylint: disable=broad-except
        print(e)
        return ['failed to parse the url, please check your url or see if the site is supported!']
    title = m.title

    if chan is None:
        # serlink = uptobox.get_link(title)
        return [f'series title: {title}, chapter total:{len(m.episodes)} ']
    chlist = chan_gen(str(chan))

    ttl = []
    # epl = [f'{epl.title}{i}' for i, epl in enumerate(m.episodes)]
    # print(epl)
    for i, ep in enumerate(m.episodes):
        # if int(re.findall(r"\d+", ep.title)[0]) not in chlist:
        if i not in chlist:
            ep.skip = True
            continue
        ttl.append(ep.title)
    #return ttl
    try:
        uptl = uptobox2.get_list(title)
    except Exception as e:
        print(e)
        uptl = []
    if f'{ttl[0]}.zip' not in uptl: #uptobox.get_list(title):
        print(f'ttl: {ttl}\ntitle: {title}\nuptl: {uptl}')
        try:
            download(m, savepath)
        except Exception as e:
            print(e)
            return ['Its broken']

        zprr = []
        for ept in ttl:
            filename = ept
            result = zpr(stitle=title,
                    filename=filename,
                    dest= f'{savepath}/{title}',
                    to_zip= f'{savepath}/{title}/{filename}'.strip())
            zprr.append(result)
        return zprr

    rlink = []
    for ch_title in ttl:
        rlink.append(f'{title} - {ch_title}')
        rlink.append(uptobox2.get_link(title, ch_title))
    return rlink

def chan_gen(strnum):
    if "," in strnum.replace(' ', ''):
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


def zpr(filename, stitle,  dest, to_zip):

    local_path = f'{dest}/zipped/{filename}'.strip()
    if not os.path.isfile(f'{local_path}.zip'):
        try:
            shutil.make_archive(f'{local_path}',
                'zip', to_zip)
        except Exception as e: # pylint: disable=broad-except
            print(e)
            return f'something wrong with {filename} \n error: {e}'
    try:

        uptobox2.upload(stitle, filename, f'{local_path}.zip')
        try:
            os.remove(f'{local_path}.zip')
        except Exception as e:
            print(e)
    except Exception as e: # pylint: disable=broad-except
        print(e)
    rlink = uptobox2.get_link(stitle, filename)
    return rlink

#TODO: centralize those quote thingy #pylint: disable=fixme

#   try:
#       with ZipFile(f'{dest}/{filename}.zip', 'w') as wzip:
#           wzip.write(to_zip)
#       return f'zipped to {dest}'
#   except Exception as e:
#       return e


if __name__ == "__main__":
    link = "https://manga.bilibili.com/detail/mc29562?from=manga_index"
    numb = "1-3"
    print(mdownload(link,numb))
#download(m, "/data/data/com.termux/files/home/developing/discord/saved")
