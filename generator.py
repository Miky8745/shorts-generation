import llm_interface as llm
import image_interface as img
import tts_interface as tts
import validators

STORY_PATH = "temp/story.txt"
PROMPTS_PATH = "temp/prompts.txt"
IMAGES_PATH = "temp/images.txt"
AUDIOS_PATH = "temp/audios.txt"

def generate_story():
    print("Generating story...", end="")
    story = llm.generate_story()
    print("Done")
    
    print(f"Saving story to: {STORY_PATH}...", end="")
    with open(STORY_PATH, "w") as f:
        f.write(story)
    print("Done")

    return story

def generate_prompts_for_story(story : str):
    print("Generating prompts...", end="")
    image = llm.generate_prompts(story)
    print("Done")

    print(f"Saving prompts to: {PROMPTS_PATH}")
    with open(PROMPTS_PATH, "w") as f:
        f.write(image)

    return image

def generate_images_from_prompts(prompts : list):
    images = []

    with open(IMAGES_PATH, "a") as f:
        for index,i in enumerate(prompts):
            print(f"\rGenerating image {index}/{len(prompts)}.", end = "")
            url = img.generate_image(i)
            path = f"temp/{index}.png"
            img.download_image(url, path)
            images.append(path)

            f.write(path + "\n")

    print("..Done")
    return images

def prepare_img_prompts(prompt : str):
    raw_prompts = prompt.strip().split("\n")
    prompts = []

    for i in raw_prompts:
        if len(i.strip()) > 1:
            prompts.append(i)

    return prompts

def generate_audio(text : str):
    print("Generating audio...", end = "")
    audios = tts.generate_paragraphs(text)
    print("Done")
    
    return audios

def create_return_dictionary(images, audios, title):
    return {"images": images, "audios": audios, "title": title}

def generate_everything():
    valid = False
    while not valid:
        story = generate_story()
        valid = validators.validate_story(story)
    
    valid = False
    while not valid:
        prompts = generate_prompts_for_story(story)
        prompts = prepare_img_prompts(prompts)
        valid = validators.validate_prompts(story, prompts)

    images = generate_images_from_prompts(prompts)

    audio = generate_audio(story)

    title = llm.generate_title(story)

    return create_return_dictionary(images, audio, title)

def load_from_memory():
    with open(IMAGES_PATH) as f:
        images = f.readlines()

    with open(AUDIOS_PATH) as f:
        audios = f.readlines()

    for i in range(len(images)):
        images[i] = images[i].strip()
        audios[i] = audios[i].strip()
        
    return create_return_dictionary(images, audios, None)

def generate_without_llm():
    data = load_from_memory()

    with open(PROMPTS_PATH) as f:
        prompts = f.read()

    images=generate_images_from_prompts(prepare_img_prompts(prompts))

    return create_return_dictionary(images, data.get("audios"), None)