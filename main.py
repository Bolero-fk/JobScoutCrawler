from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import os
import json
import getpass

options = webdriver.ChromeOptions()
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('headless')

new_driver = ChromeDriverManager().install()
service = Service(executable_path=new_driver)
browser = webdriver.Chrome(service=service, options=options)

ACCOUNT_PATH = "private/account.json"

LOGIN_URL = "https://paiza.jp/sign_in"

def save_account_as_json():
    # ユーザーからの入力を受け付ける
    email = input("メールアドレスを入力してください: ")
    password =  getpass.getpass("パスワードを入力してください: ")

    # 入力されたデータを辞書に格納
    data = {
        "email": email,
        "password": password
    }

    # データをJSONファイルに保存
    with open(ACCOUNT_PATH, "w") as f:
        json.dump(data, f)

def load_account_from_json():
    # ファイルからJSONデータを読み込み
    with open(ACCOUNT_PATH, 'r') as f:
        data = json.load(f)

    # メールアドレスとパスワードを取得
    email = data['email']
    password = data['password']

    return email, password


def get_account():

    if not os.path.exists(ACCOUNT_PATH):
        save_account_as_json()

    return load_account_from_json()

LOGIN_EMAIL, LOGIN_PASS = get_account()

# URLを開く
browser.implicitly_wait(10)

browser.get(LOGIN_URL)

# ユーザー名を入力
browser.find_element('css selector', 'input[type="email"]').send_keys(LOGIN_EMAIL)

# パスワードを入力
browser.find_element('css selector', 'input[type="password"]').send_keys(LOGIN_PASS)

# ログインボタンをクリック
browser.find_element('css selector', 'input[type="submit"]').click()

time.sleep(2)

MESSAGE_URL = "https://paiza.jp/messages"
browser.get(MESSAGE_URL)

time.sleep(2)

# スクロール可能な要素を取得する
scrollable_form = browser.find_elements(By.CLASS_NAME, "ScoutMessagesScrollableFrame")[0]

# スクロール可能な要素までスクロールする
# scrollable_element.click()

# スクロール可能な要素の高さを取得する
scrollable_element_height = scrollable_form.size['height']

# スクロール量を設定する
scroll_amount = 1000

# xxx件と書かれているのでここから件を除いた数字がメッセージの数
message_num = int(browser.find_elements(By.CLASS_NAME, "ScoutMessagesCountNum")[0].text[:-1])

scaut_cards = browser.find_elements(By.CLASS_NAME, "MessageCard")

loop_count = 0

loop_max = 1000

# スクロール可能な要素を最下部までスクロールする
while len(scaut_cards) != message_num and loop_count < loop_max:
    
    # スクロール可能な要素の現在位置を取得する  
    current_position = browser.execute_script('return arguments[0].scrollTop', scrollable_form)
    
    # スクロール可能な要素を指定量だけスクロールする
    browser.execute_script(f'arguments[0].scrollTop = {current_position + scroll_amount}', scrollable_form)
    
    # スクロールした後に読み込みが完了するまで少し待つ
    time.sleep(1)

    scaut_cards = browser.find_elements(By.CLASS_NAME, "MessageCard")

    loop_count += 1

browser.save_screenshot('result.png')

browser.quit()
