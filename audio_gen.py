import pandas as pd
import pyttsx3


def generate_audio(text, gender="male"):
    """
    Generates audio clips of text, separated by paragraphs

    Argument:
    text (string): text to be converted to audio
    gender (string): voice's gender ("male" or "female")
    """
    print("audio_gen - Generating audio")
    # split text into paragraphs and remove whitespace
    audio_list = []
    paragraphs = text.split('\n')
    paragraphs = [i for i in paragraphs if i not in ['', ' ']]
    # get gender
    gender_select = 0
    if (gender == "female"):
        gender_select = 1
    else:
        print("Invalid voice_gender value. Select \"male\" or \"female\"")
    # generate audio with pyttsx3 for each paragraph and save to file
    engine = pyttsx3.init()
    engine.setProperty('voice', engine.getProperty('voices')[gender_select].id)
    for i in range(len(paragraphs)):
        engine.save_to_file(paragraphs[i], 'media/audio' + str(i) + '.mp3')
        engine.runAndWait()
        audio_list.append('media/audio' + str(i) + '.mp3')
    print("audio_gen - Done")
    return audio_list
