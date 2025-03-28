from moviepy.editor import *
from moviepy.video.fx.all import crop
from moviepy.video.fx import all as vfx
import random
import imk_config
from mutagen.mp3 import MP3
import subtitles

imk_config.configure_moviepy()

MUSIC = ["aPufino - Enlivening (freetouse.com).mp3", "aPufino - Magnificent (freetouse.com).mp3"]

FINAL_AUDIO_PATH = "temp/vid_audio.mp3"

def create_audio_clip(path : str):
    return AudioFileClip(path.strip())

def create_audio(audios):
    voice = concatenate_audioclips(audios)

    background = random.choice(MUSIC)
    background_duration = MP3(background).info.length

    music_point = random.randint(0, int(background_duration - voice.duration)-2)
    music_clip = AudioFileClip(background).subclip(music_point, music_point + voice.duration).volumex(0.3)

    audio = CompositeAudioClip([voice, music_clip])
    return audio, background

def zoom_in(t, duration):
    return (t / (duration * 2)) + 2

def zoom_out(t, duration):
    return ((duration - t) / (duration * 2)) + 2

def create_video(images : list[str], audios : list[AudioFileClip]):
    video_clips = []
    for i in range(len(images)):
        duration = audios[i].duration
        
        # Ensure image exists and has valid dimensions
        try:
            clip = ImageClip(images[i], duration=duration)
        except Exception as e:
            print(f"Error loading image {images[i]}: {e}")
            continue  # Skip this image if there's an error
        
        # Check image size before applying any transformations
        if clip.size[0] <= 0 or clip.size[1] <= 0:
            print(f"Invalid image size for {images[i]}. Skipping this image.")
            continue

        zoom = True
        if zoom:
            clip = clip.fx(vfx.resize, lambda t: zoom_in(t,duration))

        # Ensure resized clip size is always positive
        if clip.size[0] <= 0 or clip.size[1] <= 0:
            print(f"After resizing, invalid size for {images[i]}. Skipping this image.")
            continue
        
        clip = clip.set_position("center")
        clip = clip.set_fps(30)
        video_clips.append(clip)

    if len(video_clips) == 0:
        raise ValueError("No valid video clips to render. Check your image inputs.")
    
    video = concatenate_videoclips(video_clips)
    return video

def get_scaled_font_size(text, max_size=40, min_size=25, scaling_factor=2):
    return max(min_size, max_size - scaling_factor * len(text))

def group_subttitles(subs):
    final_subs = []
    chain = None
    for i in subs:
        if chain is None:
            chain = i
            continue
        
        add = 5 if len(chain.text) <= 3 else len(chain.text)

        if len(chain.text) + add < 16:
            chain.text += i.text
            chain.end = i.end

        else:
            final_subs.append(chain)
            chain = i

    return final_subs

def add_subtitles(clip, subs) -> CompositeVideoClip:
    sub_clip_list = []

    for i in subs:
        font_size = get_scaled_font_size(i.text)

        subtitle = TextClip(i.text, fontsize=font_size, color="white", font="Montserrat", size=(1080, None))
        subtitle = subtitle.set_position(("center", "bottom")).set_start(i.start).set_end(i.end)

        sub_clip_list.append(subtitle)

    #(w, h) = clip.size
    clip_with_subtitles = CompositeVideoClip([clip.set_position("center")] + sub_clip_list, (1080,1920))
    #clip_with_subtitles = crop(clip_with_subtitles, width=1080, height=1920, x_center=w/2, y_center=h/2)

    clip_with_subtitles = clip_with_subtitles.set_fps(30)

    return clip_with_subtitles

def render_video(images, audios):
    audio_clips = []

    for i in audios:
        audio_clips.append(create_audio_clip(i))
    
    audio, background = create_audio(audio_clips)
    audio.write_audiofile(FINAL_AUDIO_PATH, fps = 16000)
    
    audio = AudioFileClip(FINAL_AUDIO_PATH)

    subs = subtitles.generate_subtitles(FINAL_AUDIO_PATH)
    subs = group_subttitles(subs)

    video = create_video(images, audio_clips)
    video = add_subtitles(video, subs)
    
    video.audio = audio
    video.write_videofile("temp/output.mp4", codec="libx264", fps=30, threads=6)

    return background