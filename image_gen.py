from PIL import Image, ImageDraw, ImageFont
import os

def generate_image(filename='media\image0.png', text="No Text Inputted", size=12):
    """Draw a text on an Image, saves it"""
    fnt = ImageFont.truetype('arial.ttf', size)
    anchor = (10,4)
    # calculate image size
    text_draw = ImageDraw.Draw(Image.new(mode = "RGB", size = (0,0)))
    bound_box = text_draw.textbbox(anchor, text, font=fnt)
    # handle image wider than 350px
    print(bound_box)
    if bound_box[2] > 350:
        width = bound_box[2]
        num_of_lines = int(width/350) + (width % 350 > 0) # round up without importing math module
        num_of_chars = len(text)
        start_of_line = 0
        end_of_line = int(num_of_chars/num_of_lines)
        for i in range(num_of_lines):
            last_space = text.rfind(' ', start_of_line, end_of_line)
            text = text[:last_space] + '\n' + text[last_space + 1:]
            start_of_line = last_space + 1
            end_of_line += int(num_of_chars/num_of_lines) - (end_of_line - last_space)
        bound_box = text_draw.textbbox(anchor, text, font=fnt)
        print(bound_box)
    if bound_box[3] > 300:
        print('this is annoying')

    # create image; image = Image.new(mode = "RGB", size = (int(size/2)*len(text),size+20), color = "white") # 4 pixels between lines
    image = Image.new(mode = "RGB", size = (bound_box[2]+anchor[0], bound_box[3]+anchor[1]+6), color = "black")
    draw = ImageDraw.Draw(image)
    # draw text
    draw.text(anchor, text, font=fnt, fill=(255,255,255))
    # save file
    image.save(filename)
    # show file
    os.system(filename)


img_text = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."

#text_on_img(text=img_text, size=16)

generate_image(text=img_text, size=16)