from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from google_auth_oauthlib.flow import InstalledAppFlow
from io import BytesIO

SCOPES = ['https://www.googleapis.com/auth/drive']

def create_service():
    flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
    creds = flow.run_local_server(port=0)
    return build('drive', 'v3', credentials=creds)

def download_file(service, file_id, file_name):
    try:
        
        file_metadata = service.files().get(fileId=file_id, fields='mimeType').execute()
        mime_type = file_metadata.get('mimeType')

        if mime_type == 'application/vnd.google-apps.document':
            
            request = service.files().export(fileId=file_id, mimeType='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
            file_name += '.docx'
        elif mime_type == 'application/vnd.google-apps.spreadsheet':
            
            request = service.files().export(fileId=file_id, mimeType='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            file_name += '.xlsx'
        elif mime_type == 'application/vnd.google-apps.presentation':
            
            request = service.files().export(fileId=file_id, mimeType='application/vnd.openxmlformats-officedocument.presentationml.presentation')
            file_name += '.pptx'
        else:
            
            request = service.files().get_media(fileId=file_id)

        fh = BytesIO()
        downloader = MediaIoBaseDownload(fd=fh, request=request)
        done = False

        while not done:
            status, done = downloader.next_chunk()
            print("Download Progress: {0}%".format(int(status.progress() * 100)))

        fh.seek(0)
        with open(file_name, 'wb') as f:
            f.write(fh.read())
        print(f"{file_name} downloaded successfully.")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == '__main__':
    service = create_service()
    file_id = '1G4vbFIqa6l0V76Ac6wy9FlDqAaD3RLUbCUWCyM34j1s'
    file_name = 'document'  
    download_file(service, file_id, file_name)
