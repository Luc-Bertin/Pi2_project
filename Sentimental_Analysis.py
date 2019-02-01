import pandas as pd
import csv
#import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
from nltk.tokenize import WordPunctTokenizer
import re
import numpy as np
from sklearn.model_selection import train_test_split
#from __future__ import division
from collections import Counter
import string
import nltk
nltk.download("stopwords")
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize,sent_tokenize
from nltk import pos_tag
from nltk .stem import wordnet
from nltk.stem import WordNetLemmatizer
import random
import sys
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
import pickle

class SentimentalAnalysis:
    """ copyright© 2019 — Victoire Linder - License MIT """
    def __init__(self, csv_tweets=''):
        self.filename, self.csv_found = self.open_csv_companies(csv_tweets)
    
    @staticmethod
    def open_csv_companies(csv_tweets):
        try:
            df = pd.read_csv(csv_tweets, encoding='utf-8', delimiter=';')
            return(df, True)
        except:
            return(0, False)
    
    def run(self):
        if self.csv_found:
            print('uyyy')
            cols = ['sentiment','id','date','query_string','user','text']
            df=pd.read_csv("ressources/training.csv",header=None, names=cols )
            df.drop(['date','query_string','user'],axis=1,inplace=True)
            df = df.rename(columns={'id': 'id_str'})
            df['place']= 'trte'
            df = df.sample(frac=1).reset_index(drop=True)
            dff =df[:15960]
            #dff['pre_clean_len'] = [len(t) for t in dff.text]
            
            #plt.style.use('fivethirtyeight')
            
            #%matplotlib inline
            #%config InlineBackend.figure_format = 'retina'
            import re
            from bs4 import BeautifulSoup
            from nltk.tokenize import WordPunctTokenizer
            tok = WordPunctTokenizer()
            
            pat1 = r'@[A-Za-z0-9_]+'
            pat2 = r'https?://[^ ]+'
            combined_pat = r'|'.join((pat1, pat2))
            www_pat = r'www.[^ ]+'
            negations_dic = {"isn't":"is not", "aren't":"are not", "wasn't":"was not", "weren't":"were not",
                            "haven't":"have not","hasn't":"has not","hadn't":"had not","won't":"will not",
                            "wouldn't":"would not", "don't":"do not", "doesn't":"does not","didn't":"did not",
                            "can't":"can not","couldn't":"could not","shouldn't":"should not","mightn't":"might not",
                            "mustn't":"must not"}
            neg_pattern = re.compile(r'\b(' + '|'.join(negations_dic.keys()) + r')\b')
            
            def tweet_cleaner_updated(text):
                soup = BeautifulSoup(text, 'lxml')
                souped = soup.get_text()
                try:
                    bom_removed = souped.decode("utf-8-sig").replace(u"\ufffd", "?")
                except:
                    bom_removed = souped
                stripped = re.sub(combined_pat, '', bom_removed)
                stripped = re.sub(www_pat, '', stripped)
                lower_case = stripped.lower()
                neg_handled = neg_pattern.sub(lambda x: negations_dic[x.group()], lower_case)
                letters_only = re.sub("[^a-zA-Z]", " ", neg_handled)
                # During the letters_only process two lines above, it has created unnecessay white spaces,
                # I will tokenize and join together to remove unneccessary white spaces
                words = [x for x  in tok.tokenize(letters_only) if len(x) > 1]
                return (" ".join(words)).strip()
            
            testing = dff.text
            test_result = []
            for t in testing:
                test_result.append(tweet_cleaner_updated(t))
            
            clean_df = pd.DataFrame(test_result,columns=['text'])
            clean_df['sentiment'] = dff['sentiment']
            clean_df.to_csv('data/modele/clean_tweet.csv',encoding='utf-8')
            csv = 'data/modele/clean_tweet.csv'
            my_df = pd.read_csv(csv,index_col=0)
            my_df.head()
            
            my_df[my_df.isnull().any(axis=1)].head()
            np.sum(my_df.isnull().any(axis=1))
            my_df.dropna(inplace=True)
            my_df.reset_index(drop=True,inplace=True)
            court =my_df
            import string
            def text_process(text):
                
                nopunc = [char for char in text if char not in string.punctuation]
                nopunc = ''.join(nopunc)
                
                return [word for word in nopunc.split() if word.lower() not in stopwords.words('english')]
            
            
            X = court['text']
            y = court['sentiment']
            bow_transformer = CountVectorizer(analyzer=text_process).fit(X)
            len(bow_transformer.vocabulary_)
            X = bow_transformer.transform(X)
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=101)
            
            
            nb = MultinomialNB()
            nb.fit(X_train, y_train)
            preds = nb.predict(X_test)
            
            
            
            filename = 'data/modele/finalized_model.sav'
            pickle.dump(nb, open(filename, 'wb'))
            
            loaded_model = pickle.load(open(filename, 'rb'))
            result = loaded_model.score(X_test, y_test)
            print(result)
            
            
            aa=pd.read_csv("data/tweets.csv", encoding='utf-8',  sep=';')
            aa['sentiment']=2
            paaa = aa.text
            test_pa = []
            for t in paaa:
                test_pa.append(tweet_cleaner_updated(t))
            aa['text']=test_pa
            
            aa.to_csv('data/modele/tweet_predict.csv',encoding='utf-8')
            wa = aa['text']
            Wa = bow_transformer.transform(wa)
            ya_hat = nb.predict(Wa)
            finala =pd.read_csv("data/modele/tweet_predict.csv" )
            finala['sentiment']= ya_hat
            finala.to_csv('data/tw_predict.csv',encoding='utf-8')
            print("check")
            return 'Analyse sentimentale terminée', True
        else:
            return 'Fichier non trouvé', False
