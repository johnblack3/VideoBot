from audio_gen import generate_audio
from image_gen import generate_image
from video_gen import generate_video
import pandas as pd
import time

# generate text
item_to_read = 3
df = pd.read_csv('df.csv')
title = df.title[item_to_read]
selftext = df.selftext[item_to_read]
text_to_read = selftext # title + "\n" +

audio_list = generate_audio(text_to_read)

time.sleep(1)

image_list = generate_image(text=text_to_read, size=16)

time.sleep(2)

print(image_list, audio_list)

generate_video('media/background_video.mp4', image_list, audio_list)