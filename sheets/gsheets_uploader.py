import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()

class GSheetsUploader:
    def __init__(self):
        self.scope = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive"
        ]
        self.creds_file = os.getenv("GOOGLE_SERVICE_ACCOUNT_FILE")
        self.sheet_id = os.getenv("GOOGLE_SHEET_ID")
        
        if not self.creds_file or not self.sheet_id:
            print("Warning: Google Sheets credentials or Sheet ID missing in .env")
            self.client = None
        else:
            self.creds = Credentials.from_service_account_file(self.creds_file, scopes=self.scope)
            self.client = gspread.authorize(self.creds)

    def upload_data(self, df, sheet_name="CAMX Outreach"):
        if not self.client:
            print("GSheets client not initialized. Skipping upload.")
            return False
            
        try:
            sh = self.client.open_by_key(self.sheet_id)
            try:
                worksheet = sh.worksheet(sheet_name)
            except gspread.exceptions.WorksheetNotFound:
                worksheet = sh.add_worksheet(title=sheet_name, rows="1000", cols="20")
            
            # Clear and update
            worksheet.clear()
            worksheet.update([df.columns.values.tolist()] + df.fillna("").values.tolist())
            print(f"Successfully uploaded {len(df)} rows to Google Sheets.")
            return True
        except Exception as e:
            print(f"Error uploading to GSheets: {e}")
            return False

if __name__ == "__main__":
    pass
