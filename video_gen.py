from moviepy.editor import ImageClip, VideoFileClip, CompositeVideoClip, AudioFileClip

def generate_video(background_video, image_list, audio_list, final_video_name='final_video'):
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

    # add background video to list for CompositeVideoClip object
    background_video_clip = VideoFileClip(background_video, audio=False).subclip(0, total_duration)
    video_and_images.insert(0, background_video_clip)
    video = CompositeVideoClip(video_and_images).subclip(0, total_duration)

    # write video object to file
    video.write_videofile('media/' + final_video_name + '.mp4')