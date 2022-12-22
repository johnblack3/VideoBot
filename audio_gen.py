import pandas as pd
import pyttsx3

def generate_audio(text):
    engine = pyttsx3.init()
    engine.save_to_file(text_to_read, 'media/audio.mp3')
    engine.runAndWait()

df = pd.read_csv('df.csv')
title = df.title[5]
selftext = df.selftext[5]
text = title + "\n" + selftext
print(text)

generate_audio(text)