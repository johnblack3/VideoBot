"""
Contains main function for generating videos

John Black
11/7/22
"""
from audio_gen import generate_audio
from image_gen import generate_image
from video_gen import generate_video
from reddit_scraper import get_icon, get_posts
import pandas as pd

def main(background_video, update_df=False, subreddit=None, post_count=10,
            listing_type='top', post_time='day', df_index=0, separate_by_sentence=True,
            font_size=16, background_video_start=0, final_image_text=None):
    """
    Main function for generating videos
    
    Arguments:
    background_video (string): name of video to be used in background (use full filename)
    update_df (bool): update pandas DataFrame (df.csv) with getposts() (default=False)
    subreddit (string): name of subreddit (default=None)
    listing_type (string): type of listings, hot, new, top, etc. (default=top)
    post_time (string): time range for posts (default=day)
    df_index (int): index of pandas DataFrame (df.csv) to use in video (default=0)
    separate_by_sentence (bool): separate images by sentence (True) or by paragraph (False) (default=True)
    font_size (int): size of font for text in images in pixels (title font size = font_size + 2) (default=16)
    background_video_start (int): start time of background video used, in seconds (default=0)
    final_image_text (string): text to be placed in final image of video (default=None)
    """

    if update_df:
        get_posts(subreddit=subreddit, count=post_count, listing=listing_type, time=post_time)

    # generate text
    df = pd.read_csv('df.csv')
    title = df.title[df_index]
    selftext = df.selftext[df_index]
    text_to_read = title + "\n" + selftext
    if separate_by_sentence:
        text_to_read = title + ".\n" + selftext

    if final_image_text:
        text_to_read += '\n' + final_image_text

    if subreddit != None and subreddit != df.subreddit[df_index]:
        print('WARNING: Subreddit name passed to main and subreddit name in df.csv do not match. Subreddit name in df.csv will be used.')
    subreddit = df.subreddit[df_index]
    username = df.author[df_index]

    if separate_by_sentence:
        # split text into sentences
        paragraphs = text_to_read.split('.')
        paragraphs = [i for i in paragraphs if i not in ['', ' ']]
        for i in range(len(paragraphs)):
            if paragraphs[i][0] == ' ':
                paragraphs[i] = paragraphs[i][1:]
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

    subreddit_icon = get_icon(subreddit=subreddit)

    audio_list = generate_audio(text_to_read)

    image_list = generate_image(text=text_to_read, font_size=font_size,
                                background_video=background_video,
                                subreddit_icon=subreddit_icon,
                                subreddit=subreddit, username=username)

    generate_video(background_video, image_list, audio_list,
                    background_video_start=background_video_start)

main(background_video=r'C:\Users\johnb\Videos\4K Video Downloader/background1.mp4',
    update_df=False,
    subreddit=None,
    post_count=10,
    listing_type='top',
    post_time='day',
    df_index=0,
    separate_by_sentence=True,
    font_size=16,
    background_video_start=0,
    final_image_text="Comment your thoughts below and follow for more similar content!")