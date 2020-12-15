import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

# define the scope
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']

# add credentials to the account
creds = ServiceAccountCredentials.from_json_keyfile_name('My Project 28526-3e10c71c36ce.json', scope)

# authorize the clientsheet 
client = gspread.authorize(creds)
# get the instance of the Spreadsheet
sheet = client.open('Dataset_fake_review')

# get the first sheet of the Spreadsheet
sheet_instance = sheet.get_worksheet(0)

# get all the records of the data
records_data = sheet_instance.get_all_records()

#stop = stopwords.words('english')
raw_review = []
for i in records_data:
    #rev = i['reviews.text']
    raw_review.append(i['reviews.text'])

fil = []
for i in range(len(raw_review)):
    word = raw_review[i]
    text_tokens = word_tokenize(word)

    tokens_without_sw = [word for word in text_tokens if not word in stopwords.words()]

    #print(tokens_without_sw)

    filtered_sentence = (" ").join(tokens_without_sw)
    fil.append(filtered_sentence)

print(fil)



    