from bs4 import BeautifulSoup
from scout import Scout

class MynaviScoutParser:
    def parse_scout(scout_html):
        soup = BeautifulSoup(scout_html, "html.parser")

        # 会社名を取得する
        company_name = soup.find('div', class_='job_description_company').text.strip()

        # 会社説明を取得する
        description = MynaviScoutParser.get_company_description(soup)

        # 年収を取得する
        salary = soup.find('div', class_='job_description_salary').text.strip()

        # 勤務地を取得する
        location = soup.find('div', class_='job_description_location').text.strip().replace('●', '').replace('\n', ' ')

        # 年収から最小値と最大値を取得する
        min_salary, max_salary = MynaviScoutParser.get_min_max_salary(salary)

        scout = Scout(company_name=company_name, min_salary=min_salary, max_salary=max_salary, location=location, description=description, site_name="mynavi")
        
        return scout
    
    def get_min_max_salary(salary_str):
        # 不要な単位を削除する
        salary_str = salary_str.replace('万', '').replace('円', '')

        # 最小値と最大値に分離する
        salary_range = salary_str.split('～')

        # 値が取得できなかった時
        if(len(salary_range) == 0 or len(salary_range) > 2):
            return "- - -", "- - -"

        # 最小値が存在する場合は取得する
        try:
            min_salary = int(salary_range[0])
        except:
            # 存在しない場合はNoneを設定する
            min_salary = "- - -"

        # 最大値が存在する場合は取得する
        try:
            max_salary = int(salary_range[1])
        except:
            # 存在しない場合はNoneを設定する
            max_salary = "- - -"
        
        return min_salary, max_salary

    def get_company_description(soup):

        title = soup.find('div', class_='job_title').text.strip() + "\n"
        labels = ''.join(['【' + label.text + '】' for label in soup.find_all('div', class_='job_label')]) + '\n'
        appeals = soup.find('div', class_='job_appeal_point').text.strip().replace('\n', ' ') + "\n"

        occupation = soup.find('div', class_='job_description_occupation').text.strip().replace('\n', ' ')

        return title + labels + appeals + occupation

