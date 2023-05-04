# VideoBot
Generates videos with text from Reddit posts (or custom text) and a voiceover (text-to-speach).

## Setup
Create userinfo.txt according to the following setup:

`userinfo.txt`
```
CLIENT_ID
SECRET_KEY
AppName/Version
username
password
```
CLIENT_ID and SECRET_KEY are used for authenticating the Reddit API call. You must create an authorized application using a Reddit username and password at https://www.reddit.com/prefs/apps to create a CLIENT_ID and SECRET_KEY. The AppName/Version line contains the name of the application and the version (Ex. MyApp/0.0.1). The username and password lines are simply the Reddit username and password used to create the authorized application.

## Installation of Libraries
Install the required packages: `pip install -r requirements.txt`

## Usage
Call `get_posts` in `reddit_scraper.py` to generate a pandas DataFrame (df.csv) containing reddit posts.

Call `main` in `main.py` to generate an mp4 video file.

Use `get_batch` in `main.py` to generate multiple mp4 video files.

More features coming soon!