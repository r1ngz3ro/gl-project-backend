import os
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow

def authenticate_google_drive():
    SCOPES = ['https://www.googleapis.com/auth/drive.file']
    creds = None
    
    # Token file path
    token_path = 'token.json'
    credentials_path = 'credentials.json'

    # Check existing token
    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)
    
    # Refresh or re-authenticate if needed
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(credentials_path, SCOPES)
            creds = flow.run_local_server(port=0)
        
        # Save credentials for next run
        with open(token_path, 'w') as token:
            token.write(creds.to_json())
    
    return build('drive', 'v3', credentials=creds)

def upload_file_to_cloud(filename):
    """Upload file to Google Drive and return shareable link."""
    try:
        # Authenticate and get Drive service
        service = authenticate_google_drive()
        
        # Prepare file metadata
        file_metadata = {
            'name': os.path.basename(filename),
            'mimeType': '*/*'  # Allow any file type
        }
        
        # Create media object
        media = MediaFileUpload(filename, resumable=True)
        
        # Upload file
        file = service.files().create(
            body=file_metadata, 
            media_body=media, 
            fields='id'
        ).execute()
        
        # Make file publicly accessible
        permission = {
            'type': 'anyone',
            'role': 'reader'
        }
        service.permissions().create(
            fileId=file.get('id'), 
            body=permission
        ).execute()
        
        # Generate shareable link
        shareable_link = f"https://drive.google.com/file/d/{file.get('id')}/view?usp=sharing"
        
        return shareable_link
    
    except Exception as e:
        print(f"Upload failed: {e}")
        return None

