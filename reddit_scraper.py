"""
Script designed to scrape reddit posts.
Used tutorial https://www.youtube.com/watch?v=FdjVoOf9HN4m

John Black
11/7/22
"""
import requests
import pandas as pd

# Personal use script (CLIENT_ID) and secret key
CLIENT_ID = 'D1Rl8K7DtN4CUNuFYHL3Xg'
SECRET_KEY = 'Kb3M76KUw2gy8jO3tiyZoIu8Wwsajg'

auth = requests.auth.HTTPBasicAuth(CLIENT_ID, SECRET_KEY)

with open('pw.txt', 'r') as f: # Get password from file
    pw = f.read()
data = {
    'grant_type': 'password',
    'username': 'sauceyramen',
    'password': pw
}

headers = {'User-Agent': 'PopularPostCompiler/0.0.1'}
res = requests.post('https://www.reddit.com/api/v1/access_token', auth=auth, data=data, headers=headers)
TOKEN = res.json()['access_token']
headers['Authorization'] = f'bearer {TOKEN}'

# Use GET /hot to get hot posts 
res = requests.get('https://oauth.reddit.com/r/confessions/hot', headers=headers, params={'limit': '10'})

# Use GET /new to get new posts, use 'after' xor 'before' param to only get posts after/before a certain post (use fullname)
res = requests.get('https://oauth.reddit.com/r/confessions/new', headers=headers, params={'limit': '10'})

# Create pandas df to store data from json (use res.json() to retrieve data)
df = pd.DataFrame()

# Add data to df; use post['data'].keys() to get all available keys
for post in res.json()['data']['children']:
    df = df.append({
        'subreddit': post['data']['subreddit'],
        'title': post['data']['title'],
        'selftext': post['data']['selftext'],
        'upvote_ratio': post['data']['upvote_ratio'],
        'ups': post['data']['ups'],
        'downs': post['data']['downs'],
        'score': post['data']['score']
    }, ignore_index=True)

df.to_csv('df.csv')

# fullname (post id)
post['kind'] + '_' + post['data']['id']