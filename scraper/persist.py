import json
import os

import gspread
from loguru import logger

from scraper.strategy import Strategy

creds_file_path = "credentials.json"
if not os.path.isfile(creds_file_path):
    logger.warning("Credential file doesn't exists")
with open(creds_file_path, "r") as f:
    creds = json.load(f)


class Google_sheet:
    def __init__(self, strategy: Strategy) -> None:
        self.email = "h-adji_tech@proton.me"
        self.rows = ["title", "url", "location", "date", "company", "company_url"]
        self.connector = gspread.service_account_from_dict(info=creds)
        self.data = []
        self.sheet = None
        self.strategy = strategy

    def __enter__(self):
        if not self.strategy.sheet_id:
            logger.info("creating new sheet")
            sheet = self.connector.create(self.strategy.sheet_name)
            self.strategy.sheet_id = sheet.id
            self.connector.insert_permission(
                file_id=sheet.id, value=self.email, perm_type="user", role="writer"
            )
            sheet.sheet1.append_row(self.rows)
        else:
            sheet = self.connector.open_by_key(key=self.strategy.sheet_id)
            self.strategy.sheet_name = sheet.title

        self.sheet = sheet.sheet1
        return self

    def __exit__(self, exc_type, exc, tb):
        if self.data:
            self.sheet.append_rows(self.data)

    def append(self, job):
        self.data.append(job)
        if len(self.data) > 20:
            self.sheet.append_rows(self.data)
            self.data = []
