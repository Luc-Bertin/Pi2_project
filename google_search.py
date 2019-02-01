from bs4 import BeautifulSoup
import requests
import regex as re
import pandas as pd
import time
import random

class BigSearchGoogle:
    """ copyright© 2019 — Luc Bertin - License MIT """
    def __init__(self, csv_file=None):
        self.csv_file=csv_file
        self.df_companies, self.df_found = self.open_csv_companies(csv_file)

    @staticmethod
    def open_csv_companies(csv_file):
        try:
            df = pd.read_csv(csv_file, encoding='utf-8', delimiter=';')
            return(df, True)
        except:
            return(0, False)

    def run(self):
        if self.df_found:
            companies_list = self.df_companies["companies"].tolist()
            companies_twitter_account = []
            progress=round(1*100/len(companies_list),2)
            
            print(companies_list)
            for companie in companies_list:
                time.sleep(random.randrange(start=7,stop=10)/10)
                print("progress : "+ str(progress) +'%')
                test = Google_Analysis(term=companie)
                companies_twitter_account.append(test.run())
                progress+=round(1*100/len(companies_list),2)
            
            print(companies_twitter_account)
            self.df_companies["twitter_account"] = companies_twitter_account
            self.df_companies = self.df_companies[['companies', 'twitter_account',\
             'location', 'nb_of_followers', 'url', 'about']]
            self.df_companies.to_csv(self.csv_file, encoding='utf-8', index=False, sep=';')
            return 'Dataframe enrichie!', True
        else:
            return 'Incorrect name or non-existent dataframe', False

class Google_Analysis:
    """ copyright© 2019 — Luc Bertin - License MIT """
    def __init__(self, term, csv_file=''):
        self.completeQuery = 'twitter.com '+str(term)
        self.encodedQuery = self.completeQuery.replace(' ','+')
        self.url = 'https://www.google.com/search?q={0}&source=lnms&tmb=nws'.format(self.encodedQuery)

    def run(self):
        soup = BeautifulSoup(requests.get(self.url).text, 'html.parser')
        pattern = re.compile(r"@[^) ]+")
        result = soup.find("h3", {'class':'r'})
        if result is not None:
            if len(pattern.findall(result.text))>0:
                #print(result)
                return(pattern.findall(result.text)[0])
        else:
            return('')

