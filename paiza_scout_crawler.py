import time
import traceback
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from paiza_scout_parser import PaizaScoutParser
from account import Account

class PaizaScoutCrawler:
    LOGIN_URL = "https://paiza.jp/sign_in"
    MESSAGE_URL = "https://paiza.jp/messages"
    SCROLL_AMOUNT = 1000
    LOOP_MAX = 30
    WAIT_TIME = 2
    IMPLICITLY_WAIT_TIME = 10

    def __init__(self):
        pass

    def get_scouts(self):
        browser = self.initialize_browser()
        try:
            print("Paizaからのスカウトを取得します")
            self.login(browser)
            scouts = self.fetch_scouts(browser)
            print("Paizaからのスカウトを取得しました")
        except Exception:
            print("Paizaからのスカウトの取得に失敗しました")
            print(traceback.format_exc())
        finally:
            browser.quit()

        return [PaizaScoutParser.parse_scout(scout) for scout in scouts]
    
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
        paize_account =  Account("paiza")

        # URLを開く
        browser.implicitly_wait(self.IMPLICITLY_WAIT_TIME)

        browser.get(self.LOGIN_URL)

        # ユーザー名を入力
        WebDriverWait(browser, self.IMPLICITLY_WAIT_TIME).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'input[type="email"]'))
        ).send_keys(paize_account.EMAIL)

        # パスワードを入力
        WebDriverWait(browser, self.IMPLICITLY_WAIT_TIME).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'input[type="password"]'))
        ).send_keys(paize_account.PASSWARD)

        # ログインボタンをクリック
        WebDriverWait(browser, self.IMPLICITLY_WAIT_TIME).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'input[type="submit"]'))
        ).click()

        # ログイン処理を待つ
        time.sleep(self.WAIT_TIME)
    
    def fetch_scouts(self, browser):

        browser.get(self.MESSAGE_URL)
        time.sleep(self.WAIT_TIME)

        # スクロール可能な要素を取得する
        scrollable_form = browser.find_element(By.CLASS_NAME, "ScoutMessagesScrollableFrame")

        # スカウトメッセージの数
        sum_message_num = int(browser.find_element(By.CLASS_NAME, "ScoutMessagesCountNum").text[:-1])

        scout_cards = scrollable_form.find_elements(By.CLASS_NAME, "MessageCard")

        # 無限ループを防ぐために最大ループ数を決めておく
        loop_count = 0

        # スクロール可能な要素を最下部までスクロールする
        while len(scout_cards) != sum_message_num and loop_count < self.LOOP_MAX:
            
            # スクロール可能な要素の現在位置を取得する  
            current_position = browser.execute_script('return arguments[0].scrollTop', scrollable_form)
            
            # スクロール可能な要素を指定量だけスクロールする
            browser.execute_script(f'arguments[0].scrollTop = {current_position + self.SCROLL_AMOUNT}', scrollable_form)
            
            # スクロールした後に読み込みが完了するまで少し待つ
            time.sleep(self.WAIT_TIME)

            scout_cards = scrollable_form.find_elements(By.CLASS_NAME, "MessageCard")
            print(sum_message_num, "件中", len(scout_cards), "件取得")

            loop_count += 1

        return [card.get_attribute('innerHTML') for card in scout_cards]
