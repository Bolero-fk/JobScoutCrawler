from bs4 import BeautifulSoup

class PaizaScautParser:
    def parse_scaut(scaut_html):
        soup = BeautifulSoup(scaut_html, "html.parser")

        # 会社名を取得する
        company_name = soup.find('div', class_='MessageCardTitleName').text.strip()

        # 会社説明を取得する
        description = soup.find('div', class_='MessageCardText').text.strip()

        # 年収を取得する
        salary = soup.select_one('.MessageCardStatusItem:nth-of-type(1)').text.strip()

        # 勤務地を取得する
        location = soup.select_one('.MessageCardStatusItem:nth-of-type(2)').text.strip()

        # 使用言語を取得する
        using_lang = soup.select_one('.MessageCardStatusItemSub').text.strip()

        # 受信日を取得する
        recieve_date = soup.find('div', class_='MessageCardDate').select("span")[0].text.strip()

        #　返信期限までの残り日数を取得する
        remaining_days = soup.find('div', class_='MessageCardDate').select("span")[1].text.strip()

        # 年収から最小値と最大値を取得する
        min_salary, max_salary = PaizaScautParser.get_min_max_salary(salary)

        # 返信期限を数値に変換する
        remaining_days = PaizaScautParser.get_remaining_days(remaining_days)

        scaut = {
            'company_name': company_name,
            'description': description, 
            'min_salary': min_salary, 
            'max_salary': max_salary, 
            'location': location, 
            'using_lang': using_lang, 
            'recieve_date': recieve_date, 
            'remaining_days': remaining_days
        }

        return scaut
    
    def get_min_max_salary(salary_str):
        # 不要な単位を削除する
        salary_str = salary_str.replace('万', '').replace('円', '')  # 単位を削除

        # 最小値と最大値に分離する
        salary_range = salary_str.split('〜')

        # 値が取得できなかった時
        if(len(salary_range) == 0 or len(salary_range) > 2):
            return None, None

        # 最小値が存在する場合は取得する
        try:
            min_salary = int(salary_range[0])
        except:
            # 存在しない場合はNoneを設定する
            min_salary = None

        # 最大値が存在する場合は取得する
        try:
            max_salary = int(salary_range[1])
        except:
            # 存在しない場合はNoneを設定する
            max_salary = None
        
        return min_salary, max_salary

    def get_remaining_days(remaining_days_str):
        # 返信期限から残り日数を取得する
        if 'まもなく削除' in remaining_days_str:
            return 1
        
        # 残り日数を取得する
        remaining_days_str = remaining_days_str.replace('残り', '')
        remaining_days_str = remaining_days_str.replace('日', '')

        return int(remaining_days_str)