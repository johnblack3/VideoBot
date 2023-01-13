# TikTokBot
Generates videos with text from Reddit posts (or custom text) and a voiceover.

## Setup
Create userinfo.txt according to the following setup:

`userinfo.txt`
```
CLIENT_ID
SECRET_KEY
username
password
```
CLIENT_ID and SECRET_KEY are used for authenticating the Reddit API call. You must create an authorized application using a Reddit username and password at https://www.reddit.com/prefs/apps to create a CLIENT_ID and SECRET_KEY. The username and password lines are simply the Reddit username and password used to create the authorized application.

## Installation of Libraries
You'll need Python 3 installed with pip. Run:

`pip install moviepy.editor`

`pip install os`

`pip install pandas`

`pip install PIL`

`pip install pyttsx3`

`pip install requests`

## Usage
Call `get_posts` in `reddit_scraper.py` to generate a pandas DataFrame (df.csv) containing reddit posts.

Call `main` in `main.py` to generate an mp4 video file.
