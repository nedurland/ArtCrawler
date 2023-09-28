import pandas as pd
import time
import json
import csv
import tweepy

# api_key = 'u8E7mIbF6vJ3ouwLNGDAc6bbF'
# api_key_secret = 'CJr6VnrP5pWorPTS5cdKxJNNBSxqRmgJlav2HNZtPLjeufk5sV'
#
# access_token = '1579414423323611136-3yg1omzFjxmfBBXeuqEPJVmEcNO6f8'
# access_token_secret = 'O6BqZLrjHGDyzdE1GFpP1kizpJmT4Cu5g1YuXcqyoUItF'

api_key = 'u8E7mIbF6vJ3ouwLNGDAc6bbF'
api_key_secret = 'CJr6VnrP5pWorPTS5cdKxJNNBSxqRmgJlav2HNZtPLjeufk5sV'

access_token = '1579414423323611136-3yg1omzFjxmfBBXeuqEPJVmEcNO6f8'
access_token_secret = 'O6BqZLrjHGDyzdE1GFpP1kizpJmT4Cu5g1YuXcqyoUItF'

auth = tweepy.OAuthHandler(api_key, api_key_secret)
auth.set_access_token(access_token, access_token_secret)

# make an API instance
api = tweepy.API(auth, wait_on_rate_limit=True)
t0 = time.time()

numDate = "29-30"
date = "(since:2022-11-29 until:2022-11-30)"  # here is where we specified what dates we wanted to crawl our data from
num_Pages = 20000

art_categories = '#art OR #artwork OR #artist OR #painting OR #drawing OR #watercolor OR #sketches OR #ceramic OR #sculpting OR #sculpture OR #photography OR #pottery OR #abstract OR #realistic OR #stylized OR #modern OR #contemporary OR #inktober'
excluded_tags = '-#furry -#porn -#hentai -#nsfw -#18+ -#onlyfans -#sex -#pornography'
search_words = art_categories, 'AND (-filter:retweets) AND (filter:images) AND (filter:safe)', date, 'AND', excluded_tags

tweets_list = tweepy.Cursor(api.search_tweets, q=search_words, count=num_Pages, lang="en", since_id=0,
                            tweet_mode="extended").items(20)

output = []
for tweet in tweets_list:
    print(tweet._json)
    print("\n\n")
    output.append(tweet._json)

with open(f'tweet{numDate}.csv', 'w', encoding="utf-8") as file:
    file.write(json.dumps(output))
with open(f'tweet{numDate}.csv', 'r', encoding="utf-8") as f:
    json = json.loads(f.read())

# data_file = open(f'tweet{numDate}.csv', 'w', encoding="utf-8")
df = pd.json_normalize(json, max_level=3)
df.to_csv(f'tweet{numDate}.csv', index= False)

t1 = time.time() - t0
print("Time elapsed: ", t1)   # CPU seconds elapsed (floating point)
