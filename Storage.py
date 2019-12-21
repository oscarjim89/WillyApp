from __future__ import print_function
import googleapiclient, httplib2, oauth2client
from googleapiclient import discovery
from httplib2 import Http
from oauth2client import file, client, tools
from apiclient.http import MediaFileUpload

class Repository():
    
    def __init__(self):              
        SCOPES = 'https://www.googleapis.com/auth/drive.appfolder'
        store = file.Storage('storage.json')
        creds = store.get()
        if not creds or creds.invalid:
            flow = client.flow_from_clientsecrets('client_id.json', SCOPES)
            creds = tools.run_flow(flow, store)
        self.__DRIVE = discovery.build('drive', 'v3', http=creds.authorize(Http()))
        
    def grabacio(self,fitxer):
        file_metadata = {'name': fitxer}
        media = MediaFileUpload(fitxer, mimetype='image/jpeg')
        file = self.__DRIVE.files().create(body=file_metadata, media_body=media, fields='id').execute()
        return file.get('id')