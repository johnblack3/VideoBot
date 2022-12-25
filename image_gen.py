from PIL import Image, ImageDraw, ImageFont
from moviepy.editor import VideoFileClip
from header_gen import generate_header
import os

def generate_image(text="No Text Inputted", font_size=12, background_video=None,
                    subreddit_icon='media/default_icon.png', subreddit='r/subreddit', username='u/username'):
    """
    Draw a text on an image and saves it
    
    Arguments:
    text (string): text to be converted to images
    font_size (int): size of text in pixels (default=12)
    background_video (file name): video to be used in the background (default=None)
    subreddit_icon (file name): subreddit icon to be used in header (default=media/default_icon.png)
    subreddit (string): name of subreddit
    username (string): name of author
    """
    image_list = []
    fnt = ImageFont.truetype('arial.ttf', font_size)
    anchor = (10,6)
    # get pixel width of background video clip
    if background_video:
        video = VideoFileClip(background_video)
        if video.size[0] > video.size[1]:
            video_width = video.size[1] * (9/16)
        else: video_width = video.size[0]
        image_width = video_width * 0.80
    else: image_width = 350
    # split text into paragraphs and remove whitespace
    paragraphs = text.split('\n')
    paragraphs = [i for i in paragraphs if i not in ['', ' ']]
    # create image for each paragraph
    for i in range(len(paragraphs)):
        # calculate image size
        text_draw = ImageDraw.Draw(Image.new(mode = "RGB", size = (0,0)))
        bound_box = text_draw.textbbox(anchor, paragraphs[i], font=fnt)
        print('paragraphs[i] (top of for): ', paragraphs[i])
        start_of_line = 0
        end_of_line = paragraphs[i].find(' ')
        for iterate in range(paragraphs[i].count(' ') + 1):
            print("TOP OF FOR LOOP ", "iteration:",iterate, " text_length:", text_draw.textlength(paragraphs[i][start_of_line:end_of_line], font=fnt), end='')
            #print("length according to bound box:", text_draw.textbbox(anchor, paragraphs[i][0:paragraphs[i].find('\n')], font=fnt), "\ntext being used:", paragraphs[i][0:paragraphs[i].find('\n')])
            if text_draw.textlength(paragraphs[i][start_of_line:end_of_line], font=fnt) < image_width: # paragraphs[i][start_of_line:end_of_line]
                previous_end_of_line = end_of_line
                end_of_line = paragraphs[i].find(' ', end_of_line+1)
                print("\nIF: ", paragraphs[i][start_of_line:end_of_line], " end_of_line:", end_of_line)
                if end_of_line == -1 and text_draw.textlength(paragraphs[i][start_of_line:end_of_line], font=fnt) < image_width: break
            else:
                print("\nELSE: ", text_draw.textlength(paragraphs[i][start_of_line:previous_end_of_line], font=fnt))
                paragraphs[i] = paragraphs[i][:previous_end_of_line] + '\n' + paragraphs[i][previous_end_of_line + 1:]
                #width_check = paragraphs[i][end_of_line + 1:]
                start_of_line = previous_end_of_line + 1
                end_of_line = previous_end_of_line + 2
                print('paragraphs[i] (bottom of else): ', paragraphs[i])
                previous_end_of_line = end_of_line
                end_of_line = paragraphs[i].find(' ', end_of_line+1)
                print("IF inside ELSE: ", paragraphs[i][start_of_line:end_of_line], end_of_line)
                previous_end_of_line = end_of_line
                end_of_line = paragraphs[i].find(' ', end_of_line+1)
                print("second 'IF' inside ELSE: ", paragraphs[i][start_of_line:end_of_line], end_of_line)

        bound_box = text_draw.textbbox(anchor, paragraphs[i], font=fnt)
        print(bound_box, i)
        
        image = Image.new(mode = "RGB", size = (bound_box[2]+anchor[0], bound_box[3]+anchor[1]+6), color = "#111110")
        draw = ImageDraw.Draw(image)
        # draw text
        draw.text(anchor, paragraphs[i], font=fnt, fill=(255,255,255))
        
        # generate header for the first paragraph (title)
        if i == 0:
            image = generate_header(subreddit_icon, title_img_obj=image, subreddit=subreddit, username=username)
        
        # save file
        image.save('media\image' + str(i) + '.png')
        image_list.append('media\image' + str(i) + '.png')

    return image_list