import time
import traceback
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from mynavi_scout_parser import MynaviScoutParser
from account import Account

class MynaviScoutCrawler:
    LOGIN_URL = "https://mynavi-job20s.jp/mypage/auth/login"
    MAX_FETCH_SCOUT_NUM = 50
    WAIT_TIME = 2
    IMPLICITLY_WAIT_TIME = 10

    def __init__(self):
        pass

    def get_scouts(self):
        browser = self.initialize_browser()
        scouts = []
        try:
            print("マイナビからのスカウトを取得します")
            self.login(browser)
            scouts = self.get_scout_cards(browser)
            print("マイナビからのスカウトを取得しました")
        except Exception:
            print("マイナビからのスカウトの取得に失敗しました")
            print(browser.find_element(By.CLASS_NAME, "job_panel_group").get_attribute('innerHTML'))
            print(traceback.format_exc())
        finally:
            browser.quit()

        return [MynaviScoutParser.parse_scout(scout) for scout in scouts]
    
    def initialize_browser(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--headless")
        new_driver = ChromeDriverManager().install()
        service = Service(executable_path=new_driver)
        browser = webdriver.Chrome(service=service, options=options)
        return browser

    def login(self, browser):

        mynavi_account =  Account("mynavi")

        # URLを開く
        browser.implicitly_wait(self.IMPLICITLY_WAIT_TIME)

        browser.get(self.LOGIN_URL)

        # ユーザー名を入力
        WebDriverWait(browser, self.IMPLICITLY_WAIT_TIME).until(
            EC.presence_of_element_located((By.NAME, 'mail'))
        ).send_keys(mynavi_account.EMAIL)

        # パスワードを入力
        WebDriverWait(browser, self.IMPLICITLY_WAIT_TIME).until(
            EC.presence_of_element_located((By.NAME, 'pass'))
        ).send_keys(mynavi_account.PASSWARD)

        # ログインボタンをクリック
        WebDriverWait(browser, self.IMPLICITLY_WAIT_TIME).until(
            EC.presence_of_element_located((By.ID, 'login_btn'))
        ).click()

        time.sleep(self.WAIT_TIME)
    
    def get_scout_cards(self, browser):

        manual_scout_cards = self.fetch_scout_cards(browser, "scout_job_list")
        ai_scout_cards = self.fetch_scout_cards(browser, "ai_job_list")

        return manual_scout_cards + ai_scout_cards

    def fetch_scout_cards(self, browser, section_id):

        scout_cards = WebDriverWait(browser, self.IMPLICITLY_WAIT_TIME).until(
            EC.presence_of_element_located((By.ID, section_id))
        ).find_elements(By.CLASS_NAME, "job_offer")

        # スカウト数が最大値を超える場合、超過分だけ後ろから削除する
        if len(scout_cards) > self.MAX_FETCH_SCOUT_NUM:
            scout_cards = scout_cards[:self.MAX_FETCH_SCOUT_NUM]

        return [card.get_attribute('innerHTML') for card in scout_cards]
