from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ["https://www.googleapis.com/auth/drive.readonly"]

SERVICE_ACCOUNT_FILE = "service_account.json"

credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE,
    scopes=SCOPES
)

drive_service = build(
    "drive",
    "v3",
    credentials=credentials
)


def search_drive(query: str):
    try:
        results = drive_service.files().list(
            q=query,
            pageSize=10,
            fields="files(id,name,mimeType,modifiedTime,webViewLink)"
        ).execute()
        return results.get("files", [])
    
    except HttpError as error:
        print(f"Google Drive API Error: {error}")
        return []