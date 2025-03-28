import faster_whisper
import faster_whisper.transcribe

class Subtitle:
    def __init__(self, text, start, end):
        self.text = text
        self.start = start
        self.end = end

ERROR_CORRECTION = 0.1

whisper = faster_whisper.WhisperModel(model_size_or_path = "base", device = "cuda", compute_type = "int8", local_files_only = True)

def generate_subtitles(path):
    subtitles = []
    
    segments, info = whisper.transcribe(path, word_timestamps=True)
    for segment in segments:
        for _, word in enumerate(segment.words):
            subtitle = Subtitle(word.word, word.start, word.end + ERROR_CORRECTION if word.end + ERROR_CORRECTION > word.start else word.end)
            subtitles.append(subtitle)
    
    return subtitles