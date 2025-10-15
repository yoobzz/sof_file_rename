import os
import pickle
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from flask import current_app

# Scopes dla Google Drive API
SCOPES = ['https://www.googleapis.com/auth/drive.file']

class GoogleDriveService:
    def __init__(self):
        self.service = None
        self.credentials = None
        
    def authenticate(self):
        """Autoryzacja z Google Drive API"""
        creds = None
        
        # Sprawdź czy istnieją zapisane credentials
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        
        # Jeśli nie ma ważnych credentials, poproś o autoryzację
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                # Sprawdź czy istnieje plik credentials
                credentials_file = current_app.config.get('GOOGLE_DRIVE_CREDENTIALS_FILE', 'credentials.json')
                if not os.path.exists(credentials_file):
                    return False, "Brak pliku credentials.json. Skonfiguruj Google Drive API."
                
                flow = InstalledAppFlow.from_client_secrets_file(
                    credentials_file, SCOPES)
                creds = flow.run_local_server(port=0)
            
            # Zapisz credentials dla następnego razu
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)
        
        self.credentials = creds
        self.service = build('drive', 'v3', credentials=creds)
        return True, "Autoryzacja pomyślna"
    
    def upload_file(self, file_path, filename, folder_id=None):
        """Upload pliku na Google Drive"""
        try:
            if not self.service:
                success, message = self.authenticate()
                if not success:
                    return False, message
            
            # Metadata pliku
            file_metadata = {
                'name': filename,
                'parents': [folder_id] if folder_id else []
            }
            
            # Upload pliku
            media = MediaFileUpload(file_path, resumable=True)
            file = self.service.files().create(
                body=file_metadata,
                media_body=media,
                fields='id,name,webViewLink'
            ).execute()
            
            return True, {
                'file_id': file.get('id'),
                'name': file.get('name'),
                'link': file.get('webViewLink')
            }
            
        except Exception as e:
            return False, f"Błąd uploadu: {str(e)}"
    
    def create_folder(self, folder_name, parent_folder_id=None):
        """Stwórz folder na Google Drive"""
        try:
            if not self.service:
                success, message = self.authenticate()
                if not success:
                    return False, message
            
            file_metadata = {
                'name': folder_name,
                'mimeType': 'application/vnd.google-apps.folder',
                'parents': [parent_folder_id] if parent_folder_id else []
            }
            
            folder = self.service.files().create(
                body=file_metadata,
                fields='id,name'
            ).execute()
            
            return True, folder.get('id')
            
        except Exception as e:
            return False, f"Błąd tworzenia folderu: {str(e)}"
    
    def search_files(self, query):
        """Szukaj plików na Google Drive"""
        try:
            if not self.service:
                success, message = self.authenticate()
                if not success:
                    return False, message
            
            results = self.service.files().list(
                q=query,
                fields="nextPageToken, files(id, name, webViewLink)"
            ).execute()
            
            return True, results.get('files', [])
            
        except Exception as e:
            return False, f"Błąd wyszukiwania: {str(e)}"
