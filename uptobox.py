import os
from dotenv import load_dotenv
import dropbox

load_dotenv()
TOKEN = os.getenv('DROPBOX_TOKEN')

dbx = dropbox.Dropbox(TOKEN)

root = '/raws'

def check_files(site, stitle):
    """ get list of files from db
    :param site: raws source
    :param stitle: series title
    :return: list of chapter zip files
    """

    flist = dbx.files_list_folder(f'{root}/{site}/{stitle}').entries
    entries = [e.name for e in flist]
    return entries


def upload(site, stitle, ctitle, local_path):
    """ Upload file to dbx
    :param site: raws source
    :param stitle: series title
    :param ctitle: chapter title
    :param local_path: path of files to upload
    :return: link to file
    """

    box_path = f'{root}/{site}/{stitle}/{ctitle}.zip'
    with open(local_path, 'rb') as f:
        dbx.files_upload(f.read(), box_path)
    return get_link(site, stitle, ctitle)


def get_link(site, stitle, ctitle=None):
    """get link for dbox file
    :param site: raws source
    :param stitle: series title
    :param ctitle: chapter title
    :return: link to file if ctitle is specified.
    :else: return folder link
    """

    box_path = f'{root}/{site}/{stitle}'
    if ctitle is None:
        link = dbx.sharing_create_shared_link(box_path).url
    else:
        link = dbx.sharing_create_shared_link(f'{box_path}/{ctitle}.zip').url
    return link


if __name__ == '__main__':

    tsite = 'tsite'
    tstitle = 'ttitle'

    # loop = asyncio.get_event_loop()
    # print(loop.run_until_complete(check_files(tsite, tstitle)))
    print(check_files(tsite, tstitle))
