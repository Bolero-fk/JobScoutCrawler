from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from account import Account

class PaizaScautCrawler:
    LOGIN_URL = "https://paiza.jp/sign_in"
    MESSAGE_URL = "https://paiza.jp/messages"

    def __init__(self):
        pass

    def get_scauts(self):
        browser = self.initialize_browser()
        try:
            self.login(browser)
            scauts = self.fetch_scauts(browser)
        finally:
            browser.quit()

        return scauts
    
    def initialize_browser(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('headless')
        new_driver = ChromeDriverManager().install()
        service = Service(executable_path=new_driver)
        browser = webdriver.Chrome(service=service, options=options)

        return browser

    def login(self, browser):
        paize_account =  Account("paiza")

        # URLを開く
        browser.implicitly_wait(10)

        browser.get(self.LOGIN_URL)

        # ユーザー名を入力
        browser.find_element('css selector', 'input[type="email"]').send_keys(paize_account.EMAIL)

        # パスワードを入力
        browser.find_element('css selector', 'input[type="password"]').send_keys(paize_account.PASSWARD)

        # ログインボタンをクリック
        browser.find_element('css selector', 'input[type="submit"]').click()

        time.sleep(2)
    
    def fetch_scauts(self, browser):

        browser.get(self.MESSAGE_URL)
        time.sleep(2)

        # スクロール可能な要素を取得する
        scrollable_form = browser.find_element(By.CLASS_NAME, "ScoutMessagesScrollableFrame")

        # スクロール量を設定する
        scroll_amount = 1000

        # スカウトメッセージの数
        sum_message_num = int(browser.find_element(By.CLASS_NAME, "ScoutMessagesCountNum").text[:-1])

        scaut_cards = scrollable_form.find_elements(By.CLASS_NAME, "MessageCard")

        # 無限ループを防ぐために最大ループ数を決めておく
        loop_count = 0
        loop_max = 30

        # スクロール可能な要素を最下部までスクロールする
        while len(scaut_cards) != sum_message_num and loop_count < loop_max:
            
            # スクロール可能な要素の現在位置を取得する  
            current_position = browser.execute_script('return arguments[0].scrollTop', scrollable_form)
            
            # スクロール可能な要素を指定量だけスクロールする
            browser.execute_script(f'arguments[0].scrollTop = {current_position + scroll_amount}', scrollable_form)
            
            # スクロールした後に読み込みが完了するまで少し待つ
            time.sleep(1)

            print(sum_message_num, "件中", len(scaut_cards), "件取得")
            scaut_cards = scrollable_form.find_elements(By.CLASS_NAME, "MessageCard")

            loop_count += 1

        return [card.get_attribute('innerHTML') for card in scaut_cards]
