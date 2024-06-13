from datetime import datetime

from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
from pydrive2.files import FileNotUploadedError

def API_GOOGLE_DRIVE_login(creds):
    """
    This function is used to login to Google Drive API
    :param creds: the path to the credentials file
    """
    GoogleAuth.DEFAULT_SETTINGS['client_config_file'] = creds
    gauth = GoogleAuth()
    gauth.LoadCredentialsFile(creds)
    
    if gauth.credentials is None:
        gauth.LocalWebserverAuth(port_numbers=[8092])
    elif gauth.access_token_expired:
        gauth.Refresh()
    else:
        gauth.Authorize()
        
    gauth.SaveCredentialsFile(creds)
    cred = GoogleDrive(gauth)
    return cred

def API_GOOGLE_DRIVE_CREATE_FILE(creds, name,data,id_folder):	
    """
    This function is used to create a file in Google Drive
    :param creds: the path to the credentials file
    :param name: the name of the file
    :param data: the content of the file
    :param id_folder: the id of the folder where the file will be created
    """
    cred = API_GOOGLE_DRIVE_login(creds)
    file = cred.CreateFile({'title': name,\
                                       'parents': [{"kind": "drive#fileLink",\
                                                    "id": id_folder}]})
    file.SetContentString(data)
    file.Upload()
    print(datetime.now(), "\tExecution API GOOGLE DRIVE CREATE FILE")

def API_GOOGLE_DRIVE_LIST_FILES(creds, id_folder, extension):
    """
    This function is used to list files in a folder in Google Drive
    :param creds: the path to the credentials file
    :param id_folder: the id of the folder
    :param extension: the extension of the files to list
    return
    return_tab : list of id of files
    """
    return_tab = []
    query_harmo = f"'{id_folder}' in parents and trashed=false"
    cred = API_GOOGLE_DRIVE_login(creds)
    files = cred.ListFile(
        {
            'q': f"{query_harmo}"
        }).GetList()

    for f in files:
        try:
            if (f['fileExtension'] == extension):
                return_tab.append(f['id'])
                print(f['title'], '\tID Drive:',f['id'], f"\tKind: {f['kind']},\tExt: {f['fileExtension']}")
        except : 
            continue
    print(datetime.now(), "\tExecution API GOOGLE DRIVE LIST FILES")
    return return_tab
	
def API_GOOGLE_DRIVE_DOWNLOAD(creds, id_file, path_output):
    """
    This function is used to download a file from Google Drive
    :param creds: the path to the credentials file
    :param id_file: the id of the file
    :param path_output: the path where the file will be saved
    """
    cred = API_GOOGLE_DRIVE_login(creds)
    file = cred.CreateFile({'id':id_file})
    name_file = file['title']
    if (":" in name_file):
        name_file=name_file.replace(":", "_")

    path_save=f"{path_output}/{name_file}"
    file.GetContentFile(path_save)
    print(datetime.now(), f"\tExecution API GOOGLE DRIVE DOWNLOAD {path_save}")
    return name_file

def API_GOOGLE_DRIVE_MOVE(creds, id_file,id_folder):
    cred = API_GOOGLE_DRIVE_login(creds)
    file = cred.CreateFile({'id': id_file})
    file['parents'] = [{"id":id_folder}]
    file.Upload()
    print(datetime.now(), f"\tExecution API GOOGLE DRIVE MOVE id:{id_file}")
