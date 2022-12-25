from PIL import Image, ImageDraw, ImageFilter, ImageFont

def generate_header(subreddit_icon, title_img_obj, subreddit='', username=''):
    """
    Creates first image (header) for video using subreddit name and icon, username, and title.
    
    Arguments:
    subreddit_icon (file name): subreddit icon (default=media/default_icon.png)
    title_img_obj (PIL.Image object): Image object that contains the title of the post
    subreddit (string): name of subreddit
    username (string): name of author
    """
    img = Image.open(subreddit_icon).convert("RGBA")
    background = Image.new("RGBA", img.size, (0,0,0,0))

    mask = Image.new("RGBA", img.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse([(0,0), (img.size)], fill='#111110', outline=None)

    circle_icon = Image.composite(img, background, mask)
    
    # add text
    subreddit_fnt = ImageFont.truetype('arial.ttf', int(img.size[1]/4))
    username_fnt = ImageFont.truetype('arial.ttf', int(img.size[1]/6))
    background_wide = Image.new("RGBA", (img.size[0]*4, img.size[1]), '#111110')
    draw_new = ImageDraw.Draw(background_wide)
    draw_new.text((img.size[0]+50, img.size[1]/6), text= 'r/' + subreddit, fill='white', font=subreddit_fnt)
    draw_new.text((img.size[0]+50, 3*img.size[1]/6), text='u/' + username, fill='grey', font=username_fnt)

    # combine
    header_img = Image.composite(circle_icon, background_wide, mask)
    header_img = header_img.resize(size=(title_img_obj.size[0], int((title_img_obj.size[0] * img.size[1]) / (img.size[0] * 4))))

    dst = Image.new('RGB', (header_img.width, header_img.height + title_img_obj.height))
    dst.paste(header_img, (0, 0))
    dst.paste(title_img_obj, (0, header_img.height))
    return dst



#generate_header('media\subreddit_icon.png', title_img_obj=, subreddit='r/funny', username='u/username')