from audio_gen import generate_audio
from image_gen import generate_image
from video_gen import generate_video
from reddit_scraper import get_icon
import pandas as pd

# generate text
item_to_read = 6
df = pd.read_csv('df.csv')
title = df.title[item_to_read]
selftext = df.selftext[item_to_read]
text_to_read = title + "\n" + selftext

subreddit = df.subreddit[item_to_read]
username = df.author[item_to_read]

paragraphs = text_to_read.split('\n')
paragraphs = [i for i in paragraphs if i not in ['', ' ']]
for i in range(len(paragraphs)):
    if len(paragraphs[i]) > 800:
        middle = int(len(paragraphs[i])/2)
        middle_period = paragraphs[i].rfind('.', 0, middle)
        first_half = paragraphs[i][0:middle_period+1]
        second_half = paragraphs[i][middle_period:-1]
        paragraphs[i] = first_half
        paragraphs.insert(i+1, second_half)
text_to_read = '\n'.join(paragraphs)

subreddit_icon = get_icon(subreddit=subreddit)

audio_list = generate_audio(text_to_read)

image_list = generate_image(text=text_to_read, font_size=16, background_video='media/background_video.mp4',
                            subreddit_icon=subreddit_icon, subreddit=subreddit, username=username)

generate_video('media/background_video.mp4', image_list, audio_list)