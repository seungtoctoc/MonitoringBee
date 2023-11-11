import cv2
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
import io
import numpy as np
import os
import pickle
import time

folder_id = ''
json_file = ''
SCOPES = ['https://www.googleapis.com/auth/drive']

token_file = '/server/token.pickle'
with open(token_file, 'rb') as token:
    credentials = pickle.load(token)
    
drive_service = build('drive', 'v3', credentials=credentials)
download_folder = "/download/npy"
downloaded_files = set(os.listdir(download_folder))

while True:
    results = drive_service.files().list(
        q = f"'{folder_id}' in parents and trashed=false",
        fields = 'files(id, name, createdTime)',
        orderBy = 'createdTime desc',
    ).execute()
    files = results.get('files', [])
    
    for file in files:
        file_id = file['id']
        file_name = file['name']
        
        if file_name not in downloaded_files:        
            if file_name.endswith('.npy'):
                print('start download', file_name)
                
                request = drive_service.files().get_media(fileId=file_id)
                io_bytes = io.BytesIO()
                downloader = MediaIoBaseDownload(io_bytes, request)
                done = False
            
                while done is False:
                    status, done = downloader.next_chunk()

                io_bytes.seek(0)
                image_data = np.load(io_bytes, allow_pickle=True)
                image_list = image_data.tolist()             
                
                for i  in range(4):
                    image = np.array(image_list[i], dtype=np.uint8)
                    
                    file_path = f'/download/image/{file_name[:-4]}_{i}.jpg'
                    cv2.imwrite(file_path, image)
                    
                with open('/download/data.txt', 'a') as file:
                    file.write(f'{file_name[:-4]}_prev_bee: {int(image_list[4])}\n')
                    file.write(f'{file_name[:-4]}_now_bee: {int(image_list[5])}\n')
                
                print('saved', file_name)
                
                # 파일 이름을 저장하여 중복 다운로드 방지
                with open(os.path.join(download_folder, file_name), 'wb') as file_obj:
                    file_obj.write(io_bytes.read())

                downloaded_files.add(file_name)
        
        else:
            print('time sleep')
            
            time.sleep(5)
            break
        