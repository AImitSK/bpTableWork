import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()


class TableManager:
    def __init__(self):
        self.x_bot_id = os.getenv('xBotId')
        self.token = os.getenv('token')
        self.workspace_id = os.getenv('workspaceId')
        self.url_endpoint = 'https://api.botpress.cloud/v1/'

        if not self.x_bot_id or not self.token or not self.workspace_id:
            raise ValueError("Bot ID, Token or Workspace ID is not set.")

    def get_table_columns(self, table_id):
        '''Get the columns of the table by analyzing the first row'''
        rows_data = self.load_table_rows(table_id)
        if rows_data and "rows" in rows_data and len(rows_data["rows"]) > 0:
            first_row = rows_data["rows"][0]
            columns = list(first_row.keys())
            return columns
        else:
            print("No rows found to extract columns.")
            return None

    def load_table_rows(self, table_id):
        '''Fetch table data from the API and handle potential errors'''
        url = f"{self.url_endpoint}tables/{table_id}/rows/find"

        payload = json.dumps({})
        headers = {
            'x-bot-id': self.x_bot_id,
            'x-workspace-id': self.workspace_id,
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.token}'
        }

        try:
            response = requests.post(url, headers=headers, data=payload, timeout=10)
            response.raise_for_status()
            return response.json()

        except requests.exceptions.Timeout:
            print("The request timed out.")

        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")

        except json.JSONDecodeError:
            print("Failed to parse response as JSON.")

        return None

    def add_row(self, table_id, row_data):
        '''Add a new row to the table with the given data'''
        url = f"{self.url_endpoint}tables/{table_id}/rows"
        headers = {
            'x-bot-id': self.x_bot_id,
            'x-workspace-id': self.workspace_id,
            'Authorization': f'Bearer {self.token}',
            'Content-Type': 'application/json'
        }

        new_row_data = {
            "rows": [row_data]
        }

        try:
            payload = json.dumps(new_row_data)
            response = requests.post(url, headers=headers, data=payload)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
            return None
