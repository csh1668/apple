import csv
import re
import os
import string
import nltk
import preprocessor.api as p
import tweepy
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

consumer_key = '7Z44N0uFgY5KWIBFi9IoyA7u4'
consumer_secret = '9ZKF4sDlFwXUchUzTRLgEmw2X3UMnEBzuCQwOWPZcedKtqLL3i'

access_token = '1033947925-lTJnqa4ukaeHiYxQohgV7ZHWZAP2w5VCbSL2um4'
access_token_secret = 'iCreMglA8shKRXutUO7AyeiQJIoI3Kq9VdmmX3aPDsWAR'

# perform authentication
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

# Create our twitter api to access tweets from it
api = tweepy.API(auth)

# Happy Emoticons
emoticons_happy = set([
    ':-)', ':)', ';)', ':o)', ':]', ':3', ':c)', ':>', '=]', '8)', '=)', ':}',
    ':^)', ':-D', ':D', '8-D', '8D', 'x-D', 'xD', 'X-D', 'XD', '=-D', '=D',
    '=-3', '=3', ':-))', ":'-)", ":')", ':*', ':^*', '>:P', ':-P', ':P', 'X-P',
    'x-p', 'xp', 'XP', ':-p', ':p', '=p', ':-b', ':b', '>:)', '>;)', '>:-)',
    '<3'
    ])

# Sad Emoticons
emoticons_sad = set([
    ':L', ':-/', '>:/', ':S', '>:[', ':@', ':-(', ':[', ':-||', '=L', ':<',
    ':-[', ':-<', '=\\', '=/', '>:(', ':(', '>.<', ":'-(", ":'(", ':\\', ':-c',
    ':c', ':{', '>:\\', ';('
    ])

#Emoji patterns
emoji_pattern = re.compile("["
                           u"\U0001F600-\U0001F64F"  # emoticons
                           u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                           u"\U0001F680-\U0001F6FF"  # transport & map symbols
                           u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           u"\U00002702-\U000027B0"
                           u"\U000024C2-\U0001F251"
                           "]+", flags=re.UNICODE)

#combine sad and happy emoticons
emoticons = emoticons_happy.union(emoticons_sad)

#mrhod clean_tweets()
def clean_tweets(tweet):
    stop_words = set(stopwords.words('english'))

    #after tweepy preprocessing the colon left remain after removing mentions
    #or RT sign in the beginning of the tweet
    tweet = re.sub(r':', '', tweet)
    tweet = re.sub(r'‚Ä¶', '', tweet)
    #replace consecutive non-ASCII characters with a space
    tweet = re.sub(r'[^\x00-\x7F]+',' ', tweet)
    #remove emojis from tweet
    tweet = emoji_pattern.sub(r'', tweet)

    word_tokens = word_tokenize(tweet)

    filtered_tweet = []

    #looping through conditions
    for w in word_tokens:
        #check tokens against stop words , emoticons and punctuations
        if w not in stop_words and w not in emoticons and w not in string.punctuation:
            filtered_tweet.append(w)
    return ' '.join(filtered_tweet)

nltk.download('stopwords')
nltk.download('punkt')

loop = True

while loop:

    print(
        '''
        1. Search tweets by keywords
        2. Exit
        ''')

    user_input = input('Enter your option: ')

    if int(user_input) == 1:
        search_term = input('Enter tweet keyword/hashtag to search: ')
        no_of_search_items = int(input('Enter number of tweets to analyze: '))
        date_since = input('Enter starting date (e.g., 2019-12-01): ')

        public_tweets = tweepy.Cursor(api.search,
                                      q=search_term,
                                      lang="en",
                                      since=date_since).items(no_of_search_items)

        index = 0
        if os.path.isfile('./tweetbykeyword.csv'):
            my_csv_file = open('tweetbykeyword.csv', 'r+')
            reader = csv.DictReader(my_csv_file)
            field_names = ['Index', 'Keyword', 'Tweets']
            for each_row in reader:
                if search_term == each_row['Keyword']:
                    index += 1
            writer = csv.DictWriter(my_csv_file, fieldnames=field_names)
        else:
            my_csv_file = open('tweetbykeyword.csv', 'w', encoding='utf8')
            field_names = ['Index', 'Keyword', 'Tweets']
            writer = csv.DictWriter(my_csv_file, fieldnames=field_names)
            writer.writeheader()

        for each_tweet in public_tweets:
            data = p.clean(each_tweet.text)
            data = clean_tweets(data)
            data = data.encode('utf-8')
            data = data.decode('unicode_escape')
            writer.writerow({'Index': index, 'Keyword': search_term, \
                             'Tweets': data})
            index += 1

    elif int(user_input) == 2:
        loop = False
    else:
        print('Please enter 1 or 2')