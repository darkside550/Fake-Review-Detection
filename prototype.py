import gspread
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
class Prototype:
    def index_brands(self):
        self.index_pos = []
        record_data = sheet_instance.col_values('1')
        
        for i in range(2,len(record_data)):
            if record_data[i] == 'OnePlus 8T':
                i += 1
                self.index_pos.append(i)
        
        return self.index_pos
    #review extraction from google sheets
    
    def review_extraction(self):
        pos_rev = []
        
        for j in self.index_pos:
            pos = f'H{str(j)}'
            pos_rev.append(pos)

        raw_review = []
        
        for i in pos_rev:
            rev_val = sheet_instance.acell(i).value
            raw_review.append(rev_val)
        #print(raw_review)
        self.word_review = []
        
        for i in range(len(raw_review)):
            word = raw_review[i]

            text_tokens = word_tokenize(word)
            
            tokens_without_sw = [word for word in text_tokens if not word in stopwords.words()]
        #   print(tokens_without_sw)
            
            filtered_sentence = (" ").join(tokens_without_sw)
            
            self.word_review.append(filtered_sentence)

        #print(self.word_review)
        return self.word_review
    
    #review is free from stopwords
    def lcs(self,X,Y):
        
        m = len(X)
        n = len(Y)
        
    # declaring the array for storing the dp values 
        L = [[None]*(n+1) for i in range(m+1)]
        for i in range(m+1): 
            for j in range(n+1): 
                if i == 0 or j == 0 : 
                    L[i][j] = 0
                elif X[i-1] == Y[j-1]: 
                    L[i][j] = L[i-1][j-1]+1
                else: 
                    L[i][j] = max(L[i-1][j] , L[i][j-1]) 
    

        return L[m][n]

    def comp_rev(self):
        v = [0] * len(self.word_review)
        for i in range(0,len(self.word_review)):
            for j in range(i+1, len(self.word_review)):
                res = self.lcs(self.word_review[i], self.word_review[j])
                if(v[i] > (res/len(self.word_review[i]))):
                    v[i] = v[i]
                else:
                    v[i] = res/len(self.word_review[i])
                if(v[j] > (res/len(self.word_review[j]))):
                    v[j] = v[j]
                else:
                    v[j] = res/len(self.word_review[j])

        print(v)

    def deviation_rate(self):
        pos_rate = []
        for j in self.index_pos:
            pos = f'G{str(j)}'
            pos_rate.append(pos)

        print(pos_rate)
        avg_rate = []
        for i in pos_rate:
            rate_val = sheet_instance.acell(i).value
            avg_rate.append(rate_val)

        #print(avg_rate)    
        sum_rating= 0
        for i in avg_rate:
            sum_rating = sum_rating + int(i)
            avg = sum_rating/len(avg_rate)

            user_rat = abs(float(i)-avg) / 5
            if user_rat > 0.4:
                print("Fake")
            else:
                print("Genuine")
prop = Prototype()
prop.index_brands()
prop.review_extraction()
prop.comp_rev()
prop.deviation_rate()