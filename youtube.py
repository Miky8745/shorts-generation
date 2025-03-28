from selenium_youtube import Youtube
import os
import sleeper

# pip install selenium_chrome
from selenium_chrome import Chrome

CREDITS = {"aPufino - Enlivening (freetouse.com).mp3": "\n\nMusic track: Enlivening by Pufino\nSource: https://freetouse.com/music\nFree Vlog Music Without Copyright",
           "aPufino - Magnificent (freetouse.com).mp3": "\n\nMusic track: Magnificent by Pufino\nSource: https://freetouse.com/music\nNo Copyright Music for Video (Free)"
           }


def upload_youtube(title, music, time):
    chrome = Chrome()

    chrome.get('https://www.youtube.com')

    sleeper.sleepUntil(time, 0)

    print("Uploading to youtube")
    
    youtube = Youtube(
        browser=chrome
    )

    upload_result = youtube.upload(os.path.abspath('temp/output.mp4'), title, 'This is a very nice story.' + CREDITS.get(music), ['shorts', 'stories', "storiesfordays"])
    return upload_result