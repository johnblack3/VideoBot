"""
Contains main function for generating videos

John Black
11/7/22
"""
from audio_gen import generate_audio
from image_gen import generate_image
from video_gen import generate_video
from reddit_scraper import get_icon, get_posts
from get_random_time import get_random_time
import os
import pandas as pd
# from pydub import AudioSegment
import datetime


def main(background_video, update_df=False, subreddit=None, post_count=10,
         listing_type='top', post_time='day', df_index=0, separate_method="sentence",
         font_size=16, background_video_start=0, final_image_text=None,
         generate_background_video_start=False, file_name='video', voice_gender="male", batch=False):
    """
    Main function for generating videos

    Arguments:
    background_video (string): name of video to be used in background (use full filename)
    update_df (bool): update pandas DataFrame (df.csv) with get_posts() (default=False)
    subreddit (string): name of subreddit (default=None)
    listing_type (string): type of listings, hot, new, top, etc. (default=top)
    post_time (string): time range for Reddit posts (default=day)
    df_index (int): index of pandas DataFrame (df.csv) to use in video (default=0)
    separate_method (string): separate images by "word", "sentence", or "paragraph" (default="sentence")
    font_size (int): size of font for text in images in pixels (title font size = font_size + 2) (default=16)
    background_video_start (int): start time of background video used, in seconds (default=0)
    final_image_text (string): text to be placed in final image of video (default=None)
    generate_background_video_start (bool): create random start time when True (default=False)
    file_name (string): name of the video file to be saved, without file extension (default=video)
    voice_gender (string): voice's gender ("male" or "female")
    batch (bool): true if main function call is part of a batch (default=False)
    """

    print("main - Running call for {} subreddit\n".format(subreddit))
    # update data frame ('df.csv') with new posts
    if update_df:
        get_posts(subreddit=subreddit, count=post_count,
                  listing=listing_type, time=post_time)
        print('df updated with subreddit:', subreddit)

    # generate text
    df = pd.read_csv('df.csv')
    title = df.title[df_index]
    selftext = df.selftext[df_index]
    if type(selftext) != str:
        print("Empty title, exiting function")
        return
    text_to_read = title + (".\n" if separate_method=="sentence" else "\n") + selftext

    # create image at end of video with custom text
    if final_image_text:
        text_to_read += '\n' + final_image_text

    # check if parameter subreddit matches the data frame
    if subreddit != None and subreddit != df.subreddit[df_index]:
        print(
            'WARNING: Subreddit name passed to main ({}) and subreddit name in df.csv ({}) do not match. Name in df.csv will be used.\n'.format(subreddit, df.subreddit[df_index]))
    subreddit = df.subreddit[df_index]
    username = df.author[df_index]

    # split by words, sentence, or paragraph
    if separate_method == "word":
        words = text_to_read.split(' ')
        for i in range(len(words)):
            words[i] = words[i].strip()
            while words[i][0] in [' ', '\'', '\"', '“', '*', '”', ')']:
                del(words[i])
                if len(words[i]) == 0:
                    break
        text_to_read = '\n'.join(words)
    elif separate_method == "sentence":
        # split text into sentences
        paragraphs = text_to_read.split('.')
        paragraphs = [i for i in paragraphs if i not in [
            '', ' ', '\'', '\"', '“', '”', ')']]
        for i in range(len(paragraphs)):
            paragraphs[i] = paragraphs[i].strip()
            # need to fix this to only remove strings that are just quotes
            while paragraphs[i][0] in [' ', '\'', '\"', '“', '*', '”', ')']:
                paragraphs[i] = paragraphs[i][1:]
            if paragraphs[i] == '':
                del (paragraphs[i])
                continue
            if i != 0 and paragraphs[i][-1] not in ['?', '!']:
                paragraphs[i] = paragraphs[i] + '.'
        text_to_read = '\n'.join(paragraphs)
    else:
        # split text into paragraphs
        paragraphs = text_to_read.split('\n')
        paragraphs = [i for i in paragraphs if i not in ['', ' ']]
        for i in range(len(paragraphs)):
            if len(paragraphs[i]) > 200:
                middle = int(len(paragraphs[i])/2)
                middle_period = paragraphs[i].rfind('.', 0, middle)
                first_half = paragraphs[i][0:middle_period+1]
                second_half = paragraphs[i][middle_period+2:]
                paragraphs[i] = first_half
                paragraphs.insert(i+1, second_half)
        text_to_read = '\n'.join(paragraphs)

    # get subreddit icon
    subreddit_icon = get_icon(subreddit)

    # generate audo
    audio_list = generate_audio(text_to_read, gender=voice_gender)

    # calculate random time to start video in background
    # total_durration = 0
    if generate_background_video_start:
        # for f in audio_list:
        #     audio = AudioSegment.from_mp3(f)
        #     audio_len = len(audio)/1000
        #     total_durration += audio_len
        background_video_start = get_random_time(
            180)  # need length of video here

    # generate images
    image_list = generate_image(text=text_to_read, font_size=font_size,
                                background_video=background_video,
                                subreddit_icon=subreddit_icon,
                                subreddit=subreddit, username=username)

    # generate video
    try:
        generate_video(background_video, image_list, audio_list,
                       background_video_start=background_video_start,
                       final_video_name=file_name)
    except Exception as e:
        error_message = str(e)

        # Create and write the error message to a file
        with open("error_message.txt", "a") as file:
            file.write(file_name + '\n' + error_message + '\n\n')

        print("Error message from subreddit {} index {}:\n".format(
            subreddit, df_index), error_message)
        return

    print("main - Done call for {} subreddit\n".format(subreddit))

    if batch:
        return audio_list, image_list
    else:
        # delete image and audio files
        for i in range(len(image_list)):
            os.remove(image_list[i])
            os.remove(audio_list[i])
        if os.path.exists('media/subreddit_icon.png'):
            os.remove('media/subreddit_icon.png')


def daily_batch(posts_from_each, subreddits):
    """
    Function for generating multiple videos (batches)

    Arguments:
    posts_from_each (int): number of posts to generate from each subreddit
    subreddit (list): list of strings containing name of subreddits (default=)
    """
    print("Starting daily_batch function with {} posts from:".format(posts_from_each))
    print("\n".join(subreddits), '\n')

    # loop through subreddits and post count
    new_df = True
    for sub in subreddits:
        for j in range(posts_from_each):
            day = datetime.datetime.now().strftime("%m-%d-%y")
            video_title = day + ' ' + sub + ' ' + str(j)
            if j == 0:
                new_df = True
            else:
                new_df = False
            audio_list, image_list = main(background_video=r'C:\Users\johnb\Videos\4K Video Downloader/19 Beautiful Minutes of Parkour.mp4',
                                          update_df=new_df,
                                          subreddit=sub,
                                          post_count=posts_from_each,
                                          df_index=j,
                                          generate_background_video_start=True,
                                          file_name=video_title,
                                          batch=True)
    # delete image and audio files
    for i in range(len(image_list)):
        os.remove(image_list[i])
        os.remove(audio_list[i])
    if os.path.exists('media/subreddit_icon.png'):
        os.remove('media/subreddit_icon.png')


# call main method
# main(background_video=r'C:\Users\johnb\Videos\4K Video Downloader/19 Beautiful Minutes of Parkour.mp4',
#      update_df=False,
#      subreddit='TrueOffMyChest',
#      post_count=10,
#      listing_type='top',
#      post_time='day',
#      df_index=0,
#      separate_method="sentence",
#      font_size=16,
#      background_video_start=0,
#      final_image_text="Thanks for watching, comment your thoughts and opinions below",
#      generate_background_video_start=True,
#      file_name=datetime.datetime.now().strftime("%m-%d-%y") + ' ' +
#      'TrueOffMyChest' + ' ' + 'manual',
#      voice_gender="female")

daily_batch(5, subreddits=['tifu', 'TrueOffMyChest', 'confessions',
            'offmychest', 'AmItheAsshole'])
