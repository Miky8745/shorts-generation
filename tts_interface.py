from TTS.api import TTS

tts = TTS(model_name="tts_models/en/vctk/vits")

def create_audio_file(text, path):
    tts.tts_to_file(text=text, file_path=path, speaker="p230")

def generate_paragraphs(text : str):
    audios = []
    paragraphs = text.split("\n")
    with open("temp/audios.txt", "a") as f:
        for index, i in enumerate(paragraphs):
            if len(i.strip()) > 1:
                path = f"temp/{index}.wav"
                create_audio_file(i, path)
                audios.append(path)

                f.write(path + "\n")

    create_audio_file(text, "temp/audio.wav")

    return audios

if __name__ == "__main__":
    create_audio_file("The quick brown fox jumps over the lazy dog. Artificial intelligence is revolutionizing the way we live and work.", "test.wav")