from moviepy.editor import ImageClip, VideoFileClip, CompositeVideoClip, AudioFileClip
import os

def generate_video(background_video, image_list, audio_list, background_video_start=0, final_video_name='final_video'):
    """
    Generates video clips with synchronized images and audio
    
    Arguments:
    background_video (string): name of video to be used in background (use full filename)
    image_list (list): list of image files
    audio (list): list of audio files
    final_video_name (string): name of video to be saved (default=final_video)
    """
    # catch error with creating image or audio files
    if len(image_list) != len(audio_list):
        return print('Image and audio list not same length')

    total_duration = 0
    previous_clip_duration = 0
    video_and_images = []

    for i in range(len(image_list)):
        # create image and audio clip objects
        image_clip = ImageClip(image_list[i]).set_position(('center', 'center'))
        audio_clip = AudioFileClip(audio_list[i])

        # set the audio, duration, and start time of the image clip
        image_clip = image_clip.set_audio(audio_clip)
        image_clip = image_clip.set_duration(audio_clip.duration) # change to set duration
        image_clip = image_clip.set_start(total_duration)
        previous_clip_duration = audio_clip.duration
        total_duration += audio_clip.duration
        video_and_images.append(image_clip)

    # create background video clip and crop to size
    background_video_clip = (VideoFileClip(background_video, audio=False)
                                .subclip(background_video_start, background_video_start + total_duration))
    if background_video_clip.w > background_video_clip.h:
        top_left_corner = int((background_video_clip.w - (9/16) * background_video_clip.h)/2)
        background_video_clip = background_video_clip.crop(x1=top_left_corner,
                                                            y1=0, 
                                                            x2=background_video_clip.w - top_left_corner, 
                                                            y2=background_video_clip.h)

    # add background video to list for CompositeVideoClip object
    video_and_images.insert(0, background_video_clip)
    video = CompositeVideoClip(video_and_images).subclip(0, total_duration)

    # write video object to file
    video.write_videofile('media/' + final_video_name + '.mp4')

    # delete image and audio files
    for i in range(len(image_list)):
        os.remove(image_list[i])
        os.remove(audio_list[i])