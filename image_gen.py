from PIL import Image, ImageDraw, ImageFont
import os

def generate_image(text="No Text Inputted", size=12):
    """Draw a text on an Image, saves it"""
    image_list = []
    fnt = ImageFont.truetype('arial.ttf', size)
    anchor = (10,4)
    # split text into paragraphs
    paragraphs = text.split('\n')
    while '' in paragraphs:
        paragraphs.remove('') # remove extra newlines
    for i in range(len(paragraphs)):
        # calculate image size
        text_draw = ImageDraw.Draw(Image.new(mode = "RGB", size = (0,0)))
        bound_box = text_draw.textbbox(anchor, paragraphs[i], font=fnt)
        # handle image wider than 300px
        print(bound_box)
        if bound_box[2] > 350:
            width = bound_box[2]
            num_of_lines = int(width/350) + (width % 350 > 0) # round up without importing math module
            num_of_chars = len(paragraphs[i])
            start_of_line = 0
            end_of_line = int(num_of_chars/num_of_lines)
            for j in range(num_of_lines):
                last_space = paragraphs[i].rfind(' ', start_of_line, end_of_line)
                paragraphs[i] = paragraphs[i][:last_space] + '\n' + paragraphs[i][last_space + 1:]
                start_of_line = last_space + 1
                end_of_line += int(num_of_chars/num_of_lines) - (end_of_line - last_space)
            bound_box = text_draw.textbbox(anchor, paragraphs[i], font=fnt)
            print(bound_box, i)
        if bound_box[3] > 350:
            print('taller than 300 px')
        # create image; image = Image.new(mode = "RGB", size = (int(size/2)*len(text),size+20), color = "white") # 4 pixels between lines
        image = Image.new(mode = "RGB", size = (bound_box[2]+anchor[0], bound_box[3]+anchor[1]+6), color = "black")
        draw = ImageDraw.Draw(image)
        # draw text
        draw.text(anchor, paragraphs[i], font=fnt, fill=(255,255,255))
        # save file
        image.save('media\image' + str(i) + '.png')
        # show file
        #os.system('media\image' + str(i) + '.png')
        image_list.append('media\image' + str(i) + '.png')
    return image_list

'''
img_text = """My sister is crying over her presents and it’s getting annoying
She’s been getting on my nerves this whole week. My sister (11) has been throwing tantrums and moping because my mum won’t get her a a frank green ($60 water bottle) along with an iPhone 14, a poppy Lismon bag and a gel nail polish kit along with some t shirts. She’s been complaining and gossiping to me about it since she’s gotten into 10 fights with my mum about it and it’s just so infuriating. I admit we’re not struggling with money but we also aren’t rich and honestly I think her reaction to not getting a water bottle is just sad."""

generate_image(text=img_text, size=16)
'''