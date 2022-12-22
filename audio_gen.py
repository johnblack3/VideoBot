import pandas as pd
import pyttsx3

def generate_audio(text):
    # split text into paragraphs
    audio_list = []
    paragraphs = text.split('\n')
    while '' in paragraphs:
        paragraphs.remove('') # remove extra newlines
    print(paragraphs)
    for i in range(len(paragraphs)):
        engine = pyttsx3.init()
        engine.save_to_file(paragraphs[i], 'media/audio' + str(i) + '.mp3')
        engine.runAndWait()
        audio_list.append('media/audio' + str(i) + '.mp3')
    return audio_list

'''
df = pd.read_csv('df.csv')
title = df.title[5]
selftext = df.selftext[5]
text = title + "\n" + selftext

generate_audio(text)'''