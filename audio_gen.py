import pandas as pd
import pyttsx3

def generate_audio(text):
    """
    Generates audio clips of text, separated by paragraphs
    
    Argument:
    text (string): text to be converted to audio
    """
    # split text into paragraphs and remove whitespace
    audio_list = []
    paragraphs = text.split('\n')
    paragraphs = [i for i in paragraphs if i not in ['', ' ']]
    # generate audio with pyttsx3 for each paragraph and save to file
    for i in range(len(paragraphs)):
        engine = pyttsx3.init()
        engine.save_to_file(paragraphs[i], 'media/audio' + str(i) + '.mp3')
        engine.runAndWait()
        audio_list.append('media/audio' + str(i) + '.mp3')
    return audio_list