import json
import os

import gspread
from google.cloud.secretmanager import SecretManagerServiceClient
from loguru import logger

from scraper.strategy import Strategy

secret_name = os.environ.get("secret_name", None)


class Google_sheet:
    def __init__(self, strategy: Strategy) -> None:
        self.email = "h-adji_tech@proton.me"
        self.rows = ["title", "url", "location", "date", "company", "company_url"]
        if secret_name:
            logger.warning(
                "Using env variable to connect to secret manager for the service account"
            )
            client = SecretManagerServiceClient()
            response = client.access_secret_version(name=secret_name)
            secret_value = response.payload.data.decode("UTF-8")
            creds = json.loads(secret_value)
            self.connector = gspread.service_account_from_dict(info=creds)
        else:
            self.connector = gspread.service_account("credentials.json")

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
