import gspread

class SpreadsheetWriter:

    def __init__(self, spread_sheet_name, work_sheet_name):
        gc = gspread.service_account(filename="./private/gspread_credentials.json")
        sh = gc.open(spread_sheet_name)

        # スプレッドシートから既存のデータを取得する
        self.worksheet = sh.worksheet(work_sheet_name)

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
    
    def is_unique(self, scout, all_data):

        if any(data.get("会社名") == scout.company_name and
            data.get("提示最低年収") == scout.min_salary and
            data.get("提示最高年収") == scout.max_salary and
            data.get("取得サイト") == scout.site_name
            for data in all_data):
            return False

        return True
    
    def write_scouts(self, scouts):
        
        if(len(self.worksheet.get_all_values()) == 0):
            self.write_header()

        # 既存のデータとの重複を避けるため、挿入するデータが既に存在するかどうかをチェックする
        existing_data = self.worksheet.get_all_records()

        add_datas = []

        for scout in scouts:
            if self.is_unique(scout, existing_data):
                add_data = scout.to_dict()
                add_datas.append(add_data)

        if add_datas:
            next_id = len(existing_data) + 1
            add_rows = [[next_id + i, *data.values()] for i, data in enumerate(add_datas)]
            self.worksheet.append_rows(add_rows)
