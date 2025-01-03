"""
Contains script designed to scrape reddit posts, get_posts(),
    and a helper function to retrieve subreddit icons, get_icon().

John Black
11/7/22
"""
import requests
import pandas as pd

# Set up userinfo.txt according to the instructions in README.md
user_info = []
with open('userinfo.txt', 'r') as f:
    for line in f:
        user_info.append(line.strip())

CLIENT_ID = user_info[0]
SECRET_KEY = user_info[1]
APP_INFO = user_info[2]

auth = requests.auth.HTTPBasicAuth(CLIENT_ID, SECRET_KEY)

data = {
    'grant_type': 'password',
    'username': user_info[3],
    'password': user_info[4]
}

headers = {'User-Agent': APP_INFO}
res = requests.post('https://www.reddit.com/api/v1/access_token',
                    auth=auth, data=data, headers=headers)
TOKEN = res.json()['access_token']
headers['Authorization'] = f'bearer {TOKEN}'


def get_posts(subreddit='Python', count=10, listing='hot', time='day'):
    """
    Use Reddit API to gather posts according to input criteria

    Arguments:
    subreddit (string): name of subreddit (default=Python)
    count (int): number of posts to retrieve (default=10)
    listing (string): type of listings, hot, new, top, etc. (default=hot)
    time (string): time range for posts (default=day)
    """
    print('get_posts - Generating df.csv')
    # Use 'after' xor 'before' param to only get posts after/before a certain post (use fullname)
    # fullname (post id): post['kind'] + '_' + post['data']['id']
    res = requests.get('https://oauth.reddit.com/r/{sub}/{lst}/?t={time}'
                       .format(sub=subreddit, lst=listing, time=time),
                       headers=headers, params={'limit': str(count)})

    # Create pandas df to store data from json (use res.json() to get data)
    # df = pd.DataFrame() # removed in pandas v2.0.0

    # Add data to df; use post['data'].keys() to get all available keys
    data = []
    for post in res.json()['data']['children']:
        data.append({
            'subreddit': post['data']['subreddit'],
            'title': post['data']['title'],
            'selftext': post['data']['selftext'],
            # 'upvote_ratio': post['data']['upvote_ratio'],
            # 'ups': post['data']['ups'],
            # 'downs': post['data']['downs'],
            # 'score': post['data']['score'],
            'author': post['data']['author']
        })

    df = pd.DataFrame(data)

    # save data frame to file
    df.to_csv('df.csv')

    print('get_posts - Done\n')


def get_icon(subreddit='confession'):
    """
    Gets icon for subreddit. Returns default icon if no icon is available.

    Argument:
    subreddit (string): name of subreddit
    """
    res2 = requests.get('https://oauth.reddit.com/r/'
                        + subreddit + '/about', headers=headers)

    subreddit_icon = res2.json()['data']['icon_img']
    if subreddit_icon:
        open('media/subreddit_icon.png', 'wb')\
            .write(requests.get(subreddit_icon).content)
        return 'media/subreddit_icon.png'
    else:
        return 'media/default_icon.png'


if __name__ == "__main__":
    get_posts(subreddit='TrueOffMyChest', count=10, listing='hot', time='day')
