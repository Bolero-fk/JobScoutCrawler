import gspread
import os
from paiza_scaut_parser import PaizaScautParser
from mynavi_scaut_parser import MynaviScautParser

class SpreadsheetWriter:

    def __init__(self, sheet_name):
        gc = gspread.service_account(filename="./private/gspread_credentials.json")
        sh = gc.open(sheet_name)

        # スプレッドシートから既存のデータを取得する
        self.worksheet = sh.worksheet('シート1')

    def write_header(self):
        self.worksheet.append_row([
            "id", 
            "会社名", 
            "提示最低年収", 
            "提示最高年収", 
            "勤務地", 
            "使用言語",
            "詳細", 
            "受信日",
            "返答期限",
            "取得サイト"
        ])
    
    def is_unique(self, scaut, all_data):

        if any(data.get("会社名") == scaut.company_name and
            data.get("提示最低年収") == scaut.min_salary and
            data.get("提示最高年収") == scaut.max_salary and
            data.get("取得サイト") == scaut.site_name
            for data in all_data):
            return False

        return True
    
    def write_scauts(self, scauts):
        # 既存のデータとの重複を避けるため、挿入するデータが既に存在するかどうかをチェックする
        existing_data = self.worksheet.get_all_records()

        add_datas = []

        for scaut in scauts:
            if self.is_unique(scaut, existing_data):
                add_data = scaut.to_dict()
                add_datas.append(add_data)

        if add_datas:
            next_id = len(existing_data) + 1
            add_rows = [[next_id + i, *data.values()] for i, data in enumerate(add_datas)]
            self.worksheet.append_rows(add_rows)
