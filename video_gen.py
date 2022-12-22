from moviepy.editor import ImageClip, VideoFileClip, CompositeVideoClip, AudioFileClip

def generate_video(background_video, image_list, audio_list):
    if len(image_list) != len(audio_list):
        return "Image and audio list not same length"

    total_duration = 0
    previous_clip_duration = 0
    video_and_images = []

    for i in range(len(image_list)):
        image_clip = ImageClip(image_list[i]).set_position(('center', 'center'))
        #image_clip = ImageClip.set_start(2)

        audio_clip = AudioFileClip(audio_list[i])

        image_clip = image_clip.set_audio(audio_clip)
        image_clip = image_clip.set_duration(audio_clip.duration) # change to set duration
        image_clip = image_clip.set_start(total_duration)

        print('image_clip.start', image_clip.start)
        print('image_clip.duration', image_clip.duration)
        print('total_duration', total_duration)
        print('audio_clip.duration', audio_clip.duration)

        previous_clip_duration = audio_clip.duration
        total_duration += audio_clip.duration

        video_and_images.append(image_clip)



    video_clip = VideoFileClip(background_video, audio=False).subclip(0, total_duration)
    video_and_images.insert(0, video_clip)

    #video_clip = video_clip.set_audio(audio_clip)

    #video = CompositeVideoClip([video_clip, # starts at t=0
                                #image_clip.set_start(0)]).subclip(0, total_duration)
    
    video = CompositeVideoClip(video_and_images).subclip(0, total_duration)

    video.write_videofile("media/final_video.mp4")

#generate_video('media/background_video.mp4')