def validate_story(story):
    if "(" in story:
        return False
    
    return True

def validate_prompts(story : str, prompts):
    split_story = story.split("\n")

    num_paragraphs = 0

    for i in split_story:
        if len(i.strip()) > 1:
            num_paragraphs += 1
    
    return num_paragraphs == len(prompts)

