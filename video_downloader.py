import yt_dlp
import pprint
from url_scraper import get_episode_URLs
from question_reader import convert_video_to_text
import os

def download_video(url, order):
    options = {
        'outtmpl': f'/home/pavlyuchenko/Desktop/NaLovu/epizody/{order}.%(ext)s',
    }

    with yt_dlp.YoutubeDL(options) as ydl:
        ydl.download([url])

    return f'/home/pavlyuchenko/Desktop/NaLovu/epizody/{order}.mp4'


def main():
    data = get_episode_URLs()

    # remove all items whose order already exists in /epizody/{order}.mp4
    for item in data:
        if (os.getcwd() + f'/home/pavlyuchenko/Desktop/NaLovu/epizody/{item["order"]}.mp4').split('/')[-1] in os.listdir('/home/pavlyuchenko/Desktop/NaLovu/epizody/'):
            print(item)
            print(os.getcwd() + f'/home/pavlyuchenko/Desktop/NaLovu/epizody/{item["order"]}.mp4').split('/')[-1]))
            print(os.listdir('/home/pavlyuchenko/Desktop/NaLovu/epizody/'))
            print("----")
            
            data.remove(item)


    for item in data:
        path = download_video(item['link'], item['order'])
        convert_video_to_text(path, item['order'])

    os.remove(path)

if __name__ == "__main__":
    main()

    # video_url = "https://tv.nova.cz/porad/na-lovu/epizoda/212766-62-dil"
    # download_video(video_url)
