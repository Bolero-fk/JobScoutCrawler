import os
import json
import getpass

class Account:
    ACCOUNT_PATH = "private/account.json"

    EMAIL = ""
    PASSWARD = ""

    def __init__(self, site_name):
        self.EMAIL, self.PASSWARD = self.get_account(site_name)
    
    def get_login_info(self):
        # ユーザーからの入力を受け付ける
        email = input("メールアドレスを入力してください: ")
        password =  getpass.getpass("パスワードを入力してください: ")

        return email, password

    def save_login_info(self, site_name, append_mode = True):
        email, password = self.get_login_info()
        
        # 入力されたデータを辞書に格納
        login_info = {
            site_name: {
            "email": email,
            "password": password
            }
        }

        if(append_mode):
            with open(self.ACCOUNT_PATH, 'r') as f:
                login_info.update(json.load(f)) 

        # データをJSONファイルに保存
        with open(self.ACCOUNT_PATH, "w") as f:
            json.dump(login_info, f)

    def load_account_from_json(self, site_name):
        # ファイルからJSONデータを読み込む
        with open(self.ACCOUNT_PATH, 'r') as f:
            login_info = json.load(f)

        # メールアドレスとパスワードを取得
        email = login_info[site_name]['email']
        password = login_info[site_name]['password']

        return email, password

    def get_account(self, site_name):

        if not os.path.exists(self.ACCOUNT_PATH):
            self.save_login_info(site_name, False)
        
        try:
            return self.load_account_from_json(site_name)
        except:
            self.save_login_info(site_name, True)
            return self.load_account_from_json(site_name)

