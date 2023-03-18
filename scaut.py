import json

class Scaut:

    def __init__(self, company_name = "- - -", min_salary = "- - -", max_salary = "- - -", location = "- - -", using_lang = "- - -", description = "- - -", recieve_date = "- - -", remaining_days = "- - -", site_name = "---"):

        self.company_name = company_name
        self.min_salary = min_salary 
        self.max_salary = max_salary
        self.location = location
        self.using_lang = using_lang
        self.description = description
        self.recieve_date = recieve_date
        self.remaining_days = remaining_days
        self.site_name = site_name

    def to_dict(self):
        scaut = {
                    'company_name': self.company_name,
                    'min_salary': self.min_salary, 
                    'max_salary': self.max_salary, 
                    'location': self.location, 
                    'using_lang': self.using_lang, 
                    'description': self.description, 
                    'recieve_date': self.recieve_date, 
                    'remaining_days': self.remaining_days,
                    'site_name': self.site_name
                }
        
        return scaut


    def to_json(self):

        return json.dumps(self.to_dict(), ensure_ascii=False)

    def __str__(self):
        
        return self.to_json()
