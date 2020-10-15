#Authenticate with Twitter
import tweepy #pip install tweepy
from tweepy import OAuthHandler

consumer_key = '[]'
consumer_secret = '[]'
access_token = '[]'
access_secret = '[]'

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

api = tweepy.API(auth)

#Function to search tweets based on a keyword
from datetime import datetime, timedelta

def search_tweets(keyword, total_tweets):
    today_datetime = datetime.today().now()
    yesterday_datetime = today_datetime - timedelta(days=1)
    today_date = today_datetime.strftime('%Y-%m-%d')
    yesterday_date = yesterday_datetime.strftime('%Y-%m-%d')
    search_result = tweepy.Cursor(api.search,
                                  q=keyword,
                                  since=yesterday_date,
                                  result_type='recent',
                                  lang='en').items(total_tweets)
    return search_result

# Function to clean tweets by removing users, numbers and links
import re #pip install regex, pip install nltk
from nltk.tokenize import WordPunctTokenizer

def clean_tweets(tweet):
    user_removed = re.sub(r'@[A-Za-z0-9]+','',tweet.decode('utf-8'))
    link_removed = re.sub('https?://[A-Za-z0-9./]+','',user_removed)
    number_removed = re.sub('[^a-zA-Z]', ' ', link_removed)
    lower_case_tweet= number_removed.lower()
    tok = WordPunctTokenizer()
    words = tok.tokenize(lower_case_tweet)
    clean_tweet = (' '.join(words)).strip()
    return clean_tweet

import httplib2
import json

from oauth2client import GOOGLE_REVOKE_URI, GOOGLE_TOKEN_URI, client
from oauth2client.client import GoogleCredentials
from pydrive.auth import GoogleAuth     #pip install -U -q PyDrive
from pydrive.drive import GoogleDrive

auth_key = {
  "client_id": "[]",
  "client_secret": "[]",
  "refresh_token": "[]"
}

credentials = client.OAuth2Credentials(
    access_token=None,
    client_id=auth_key['client_id'],
    client_secret=auth_key['client_secret'],
    refresh_token=auth_key['refresh_token'],
    token_expiry=None,
    token_uri=GOOGLE_TOKEN_URI,
    user_agent=None,
    revoke_uri=GOOGLE_REVOKE_URI)

credentials.refresh(httplib2.Http())
credentials.authorize(httplib2.Http())
cred = json.loads(credentials.to_json())
cred['type'] = 'authorized_user'

with open('adc.json', 'w') as outfile:
  json.dump(cred, outfile)

import json
my_j={"type": "[]",
"project_id": "[]",
"private_key_id": "[]",
"private_key": "-----BEGIN PRIVATE KEY-----[]=\n-----END PRIVATE KEY-----\n",
"client_email": "[]",
"client_id": "[]",
"token_uri": "[]",
"auth_provider_x509_cert_url": "[]",
"client_x509_cert_url": "[]"}

with open('cred.json', 'w') as json_file:
    json.dump(my_j, json_file)

#Function to get sentiment score using Google NLP API
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types
import os
from google.oauth2 import service_account

credentials = service_account.Credentials.from_service_account_file("cred.json")

def get_sentiment_score(tweet):
    client = language.LanguageServiceClient(credentials=credentials)
    document = types\
               .Document(content=tweet,
                         type=enums.Document.Type.PLAIN_TEXT)
    sentiment_score = client\
                      .analyze_sentiment(document=document)\
                      .document_sentiment\
                      .score
    return sentiment_score

# Function to search for n tweets with keyword and return T-test scores
import numpy as np
from scipy import stats

def get_stats (keyword, n):
  tweets = search_tweets(keyword, n)
  score_array = []
  for tweet in tweets:
    global cleaned_tweet
    cleaned_tweet = clean_tweets(tweet.text.encode('utf-8'))
    global sentiment_score
    sentiment_score = get_sentiment_score(cleaned_tweet)
    print('Tweet: {}'.format(cleaned_tweet))
    print('Score: {}\n'.format(sentiment_score))
    score_array = np.append(score_array, sentiment_score)

  t_score, p_value = stats.ttest_1samp(score_array, 0)
  final_tweets = 'Tweet: {}'.format(cleaned_tweet), 'Score: {}\n'.format(sentiment_score)

  return t_score, p_value
  return cleaned_tweet, sentiment_score

word = "Dak Prescott"
qty = 5
t, p = get_stats (word, qty)
print ('T-score = ' + str(t))
print ('P Value = ' + str(p))

# START OF TKINTER GUI----------------------------------------------------------------------------------
from tkinter import * #import gui tools / pip install tk-tools
from PIL import ImageTk, Image # import python image library (pillow) / pip install Pillow

root = Tk()
root.title('Twitter Sentiment Analysis Application') #title of window
root.iconbitmap('c:/Users/jaygi/Downloads/birdy.ico') # path to icon

#add an image (page logo)
image_0 = ImageTk.PhotoImage(Image.open('c:/Users/jaygi/Downloads/app_banner.PNG')) # path to logo image (PNG)
label_0 = Label(image = image_0)    # assign the image
label_0.grid(row = 0, column = 0)   # position the image

# Define Functions ------------------------------------------------------------

def button_clear():                 # function to clear text field
    e.delete(0, END)
    q.delete(0, END)

def button_submit():                # function to submit text entries
    global word                    # make the variable callable outside the function
    word = e.get()                  # define the keyword from user entry 
    global qty
    qty = q.get()                   # define the quanity of tweets analyzed 

# Define Frames ----------------------------------------------------------------

# Frame for user input section
frame_0 = LabelFrame(root,          # define frame
text = 'Get Latest Analysis',       # add frame text
padx = 10, pady = 5,                # add frame padding (empty space surrounding)
bg = 'white', fg = 'black'          # add frame color
)
frame_0.grid(row = 1, column = 0,   # position the frame
 padx = 10, pady = 10,              # frame padding
columnspan = 10                     # match widget width to window
)   

# Frame Around Results Section 
frame_1 = LabelFrame(root,            # define frame
text = 'Twitter\'s Latest Results',   # add frame text
padx = 10, pady = 5,                  # add frame padding (empty space surrounding)
bg = 'white', fg = 'black'            # add frame color
)
frame_1.grid(row = 9, column = 0,     # position the frame
 padx = 10, pady = 10,                # frame padding
sticky = E+W,                         # match widget width to window
rowspan = 55
) 

# Frame Around Information Section 
frame_2 = LabelFrame(root,          # define frame
text = 'Definitions',               # add frame text
padx = 10, pady = 5,                # add frame padding (empty space surrounding)
bg = 'white', fg = 'black'          # add frame color
)
frame_2.grid(row = 6, column = 0,   # position the frame
 padx = 10, pady = 10,              # frame padding
columnspan = 10                     # match widget width to window
) 

# User Input Widgets (text entry fields)----------------------------------------

# keyword entry wiget 
e = Entry(frame_0,                     # define text input box
width = 60,                            # text box width 
borderwidth = 10)                      # text box border 
e.grid(row = 2, column = 0             # position the text box
)
e.insert(0, "Enter your keyword here") # default text inside text box

# quanity entry wiget 
q = Entry(frame_0,                      # define text input box
width = 60,                             # text box width 
borderwidth = 10)                       # text box border 
q.grid(row = 3, column = 0              # position the text box
)                                       # default text inside text box
q.insert(0, "Enter number of tweets to retrieve (limit of 50)") 

# Buttons ----------------------------------------------------------------------

# button widget to submit user input
button_0 = Button(frame_0,           # define buton
text = 'Return Results',             # button text
command = (button_submit,
search_tweets,
clean_tweets,
get_sentiment_score,
get_stats)        # button function  
)
button_0.grid(row = 4, column = 0,   # position the button
sticky = W+E                         # match button width to frame
) 

# button widget to clear text field
button_0 = Button(frame_0,           # define buton
text = 'Clear Text Field',           # button text
command = button_clear               # button function 
)
button_0.grid(row = 5, column = 0,  # position the button
sticky = W+E                        # match button width to frame
) 

# Labels -----------------------------------------------------------------------

# Definitions of statistical scores 

label_0 = Label(frame_2,              # Lable for mean
text =                                # text for label
'Sentiment mean is the average sentiment of all tweets referenced' ,
bg = "white"                          #color of label background
)
label_0.grid(row = 7, column = 0)     # position of label

label_1 = Label(frame_2,              # Lable for T-Score defined
text =                                # text for label
'T-score is standard deviation; the average difference of each score from the mean' ,
bg = "white"                          #color of label background
)
label_1.grid(row = 8, column = 0)     # position of label

label_2 = Label(frame_2,              # Lable for P-Score defined
text =                                # text for label
'P-value details statistical significance; p-value > 0.05 = statistical significance' ,
bg = "white"                          #color of label background
)
label_2.grid(row = 9, column = 0)     # position of label

# Results from the API

label_3 = Label(frame_1,              # Lable for T-Score results
text = 'T-score = ' + str(t) ,        # text for label
bg = "white"                          # color of label background
)
label_3.grid(row = 10, column = 0)     # position of label

label_4 = Label(frame_1,              # Lable for P-Score results
text ='P Value = ' + str(p) ,         # text for label
bg = "white"                          # color of label background
)
label_4.grid(row = 11, column = 0)    # position of label

label_5 = Label(frame_1,                         # Lable for results
text = str(('Tweet: {}'.format(cleaned_tweet)) + # Print formated tweets 
(' Score: {}\n'.format(sentiment_score))),       # Print formated scores with tweet   
bg = "white",                                    # color of label background
)
label_5.grid(row = 12, column = 0,               # position the label
sticky = N+S+E+W, 
rowspan = 50                          
)     

# End of Labels ----------------------------------------------------------------

root.mainloop() #create the event loop