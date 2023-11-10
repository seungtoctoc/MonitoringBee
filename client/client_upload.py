from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2 import service_account
import os
import time

file_folder = '/home/stt-pi/upload'
json_file = "/home/stt-pi/"

SCOPES = ['https://www.googleapis.com/auth/drive']
folder_id = ''
credentials = service_account.Credentials.from_service_account_file(json_file, scopes=SCOPES)
service = build('drive', 'v3', credentials = credentials)

if __name__ == '__main__':
    time.sleep(5)
    
    while True :
        file_list = os.listdir(file_folder)

        if not file_list:
            time.sleep(5)

        else :
            for file_name in file_list:
                file_path = os.path.join(file_folder, file_name)
                
                if os.path.isfile(file_path):
                    file_data = {'name': file_name, 'parents': [folder_id]}
                    media = MediaFileUpload(file_path, mimetype='application/octet-stream')
                    file_drive = service.files().create(body=file_data, media_body=media, fields='id').execute()
            
                    os.remove(file_path)