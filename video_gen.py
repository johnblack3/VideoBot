from moviepy.editor import ImageClip, VideoFileClip, CompositeVideoClip, AudioFileClip

def generate_video(background_video):
    image_clip = ImageClip('media/image0.png').set_position(('center', 'center'))
    #image_clip = ImageClip.set_start(2)

    audio_clip = AudioFileClip("media/audio.mp3")

    video_clip = VideoFileClip(background_video, audio=False).subclip(0, audio_clip.duration)

    video_clip = video_clip.set_audio(audio_clip)

    video = CompositeVideoClip([video_clip, # starts at t=0
                                image_clip.set_start()]).subclip(0, audio_clip.duration)

    video.write_videofile("media/final_video.mp4")

generate_video('media/background_video.mp4')