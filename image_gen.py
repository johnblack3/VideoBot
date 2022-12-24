from PIL import Image, ImageDraw, ImageFont
from moviepy.editor import VideoFileClip
import os

def generate_image(text="No Text Inputted", size=12, background_video=None):
    """
    Draw a text on an image and saves it
    
    Arguments:
    text (string): text to be converted to images
    size (int): size of text in pixels (default=12)
    background_video (file name): video to be used in the background (default=None)
    """
    image_list = []
    fnt = ImageFont.truetype('arial.ttf', size)
    anchor = (10,6)
    # get pixel width of background video clip
    if background_video:
        video = VideoFileClip(background_video)
        video_width = video.size[0]
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
        # handle image wider than image_width
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
        
        # create image; image = Image.new(mode = "RGB", size = (int(size/2)*len(text),size+20), color = "white")
        image = Image.new(mode = "RGB", size = (bound_box[2]+anchor[0], bound_box[3]+anchor[1]+6), color = "black")
        draw = ImageDraw.Draw(image)
        # draw text
        draw.text(anchor, paragraphs[i], font=fnt, fill=(255,255,255))
        # save file
        image.save('media\image' + str(i) + '.png')
        image_list.append('media\image' + str(i) + '.png')
    return image_list