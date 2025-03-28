import os
import shutil
import generator
import create_video
import time
import youtube

def cleanup():
    shutil.rmtree("temp")

def prepare(clean):
    if clean:
        cleanup()
        os.mkdir("temp")

def main():
    clean = True #input("Use existing data? [y/n]").strip().lower() != "y"
    prepare(clean)

    start = time.time()
    if clean:
        data = generator.generate_everything()
    
    else:
        images = input("Do you want to use the same images? [y/n]").strip().lower() != "n"
        
        if images:
            data = generator.load_from_memory()
        else:
            data = generator.generate_without_llm()
    
    music = create_video.render_video(data.get("images"), data.get("audios"))
    print(f"Video generated in: {time.time() - start}s")

    permission_to_upload = True #input("Do I have permission to upload? [y/n]").strip().lower() != "n"
    if not permission_to_upload:
        return
    
    target_time = 20 #int(input("What time should I upload at? [hour]"))
    
    result = youtube.upload_youtube(data.get("title"), music, target_time)
    
    print(f"Uploaded to youtube with result: {result}")

if __name__ == "__main__":
    main()