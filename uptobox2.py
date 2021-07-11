import os
import dropbox
#from dotenv import load_dotenv

#load_dotenv()
#TOKEN = os.getenv('DROPBOX_TOKEN')
TOKEN = os.environ.get('DROPBOX_TOKEN')

dbx = dropbox.Dropbox(TOKEN)


def get_list(title):
    entries = []
    try:
        for e in dbx.files_list_folder(f'/raws/{title}').entries:
            entries.append(e.name)
    except Exception as e:
        print(e)
    return entries

def upload(stitle, ch_title, local_path):
    box_path = f'/raws/{stitle}/{ch_title}.zip'
    with open(local_path, 'rb') as f:
        dbx.files_upload(f.read(), box_path)
    link = dbx.sharing_create_shared_link(box_path).url
    return link

def get_link(stitle, ch_title=None):
    if ch_title is None:
        link = dbx.sharing_create_shared_link(f'/raws/{stitle}').url
    else:
        link = dbx.sharing_create_shared_link(f'/raws/{stitle}/{ch_title}.zip').url
    return link



#dbx.users_get_current_account()

#dbx.files_create_folder('/raws')

#with open(r'./driveup.py', 'rb') as f:
#    dbx.files_upload(f.read(), '/raws/test/driveup.py')


#for entry in dbx.files_list_folder('/raws/test').entries:
#    print(f'{entry.name}, \n {entry}')
#print('share link \n \n')
#print(dbx.sharing_create_shared_link('/raws/test/driveup.py').url)
