from PIL import Image, ImageDraw, ImageFilter, ImageFont

def generate_header(subreddit_icon, title_img_obj, subreddit='subreddit', username='username'):
    """
    Creates first image (header) for video using subreddit name and icon, username, and title.
    
    Arguments:
    subreddit_icon (file name): subreddit icon (default=media/default_icon.png)
    title_img_obj (PIL.Image object): Image object that contains the title of the post
    subreddit (string): name of subreddit
    username (string): name of author
    """
    header_width = title_img_obj.size[0]
    header_height = int(header_width/7)

    # create Image objects for icon and background
    img = Image.open(subreddit_icon).convert("RGBA")
    background = Image.new("RGBA", img.size, '#111110')
    mask = Image.new("RGBA", img.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse([(0,0), (img.size)], fill='#111110', outline=None)

    # create circular icon and resize
    circle_icon = Image.composite(img, background, mask)
    circle_icon = circle_icon.resize(size=(int(header_width/12), int(header_width/12)))
    circle_icon_center = int(header_height/2) - int(circle_icon.height/2)

    # create ImageFont objects
    subreddit_fnt = ImageFont.truetype('arial.ttf', 16)
    username_fnt = ImageFont.truetype('arial.ttf', 14)

    # add text to header background
    header_background = Image.new("RGBA", (header_width, header_height), '#111110')
    draw_text = ImageDraw.Draw(header_background)
    draw_text.text((circle_icon.width + 2*circle_icon_center, int(circle_icon_center/2) + 1), text= 'r/' + subreddit, fill='white', font=subreddit_fnt)
    draw_text.text((circle_icon.width + 2*circle_icon_center, int(header_background.height/2) + 2), text='u/' + username, fill='grey', font=username_fnt)

    # combine header and title
    dst = Image.new('RGB', (header_width, header_background.height + title_img_obj.height), '#111110')
    dst.paste(header_background, (0, 0))
    dst.paste(circle_icon, (circle_icon_center, circle_icon_center))
    dst.paste(title_img_obj, (0, header_background.height))
    dst.save('media/header.png')
    return dst

if __name__ == "__main__":
    title_img_obj = Image.new("RGBA", size=(328, 50))
    generate_header('media\subreddit_icon.png', title_img_obj, subreddit='funny', username='username')