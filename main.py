from audio_gen import generate_audio
from image_gen import generate_image
from video_gen import generate_video
import pandas as pd
import time

# generate text
df = pd.read_csv('df.csv')
title = df.title[5]
selftext = df.selftext[5]
text_to_read = selftext # title + "\n" + 

generate_audio(text_to_read)

time.sleep(1)

generate_image(filename='media\image0.png', text=text_to_read, size=16)

time.sleep(2)

generate_video('media/tiktokdownload.mp4')