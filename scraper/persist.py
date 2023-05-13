import json
import os

import gspread
from google.cloud.secretmanager import SecretManagerServiceClient
from google.oauth2 import service_account
from loguru import logger

from scraper.strategy import Strategy

local_creds = service_account.Credentials.from_service_account_file("credentials.json")
secret_name = os.environ.get("secret_name", None)
if not secret_name:
    logger.warning(
        "The secrect name was not loaded make you the env variable 'secret_name' is injected in the environment"
    )
secret_name = "projects/981650884874/secrets/sheet_api_creds/versions/1"
client = SecretManagerServiceClient(credentials=local_creds)
response = client.access_secret_version(name=secret_name)
secret_value = response.payload.data.decode("UTF-8")
creds = json.loads(secret_value)


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
