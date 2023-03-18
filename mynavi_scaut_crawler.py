from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time
from mynavi_scaut_parser import MynaviScautParser
from account import Account

class MynaviScautCrawler:
    LOGIN_URL = "https://mynavi-job20s.jp/mypage/auth/login"

    def __init__(self):
        pass

    def get_scauts(self):
        browser = self.initialize_browser()
        try:
            self.login(browser)
            scauts = self.fetch_scauts(browser)
        finally:
            browser.quit()

        return [MynaviScautParser.parse_scaut(scaut) for scaut in scauts]
    
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
        mynavi_account =  Account("mynavi")

        # URLを開く
        browser.implicitly_wait(10)

        browser.get(self.LOGIN_URL)

        # ユーザー名を入力
        browser.find_element('css selector', 'input[name="mail"]').send_keys(mynavi_account.EMAIL)

        # パスワードを入力
        browser.find_element('css selector', 'input[name="pass"]').send_keys(mynavi_account.PASSWARD)


        # ログインボタンをクリック
        browser.find_element(By.ID, 'login_btn').click()

        time.sleep(2)
    
    def fetch_scauts(self, browser):

        MAX_FETCH_SCAUT_NUM = 50

        manual_scaut_cards = browser.find_element(By.ID, "scout_job_list").find_elements(By.CLASS_NAME, "job_offer")

        # スカウト数が最大値を超える場合、超過分だけ後ろから削除する
        if len(manual_scaut_cards) > MAX_FETCH_SCAUT_NUM:
            manual_scaut_cards = manual_scaut_cards[:MAX_FETCH_SCAUT_NUM]

        ai_scaut_cards = browser.find_element(By.ID, "ai_job_list").find_elements(By.CLASS_NAME, "job_offer")
        
        # スカウト数が最大値を超える場合、超過分だけ後ろから削除する
        if len(ai_scaut_cards) > MAX_FETCH_SCAUT_NUM:
            ai_scaut_cards = ai_scaut_cards[:MAX_FETCH_SCAUT_NUM]

        return [card.get_attribute('innerHTML') for card in manual_scaut_cards + ai_scaut_cards]
