# from webnovel_tts import convert
# from my_webnovel_scrape import download_text
# from my_webnovel_scrape import download_audio
import os
from urllib.parse import urlsplit
# from gtts import gTTS
import time
from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin


def main():
    if os.path.exists('next_link.txt'):
        with open('next_link.txt', 'r') as file:
            link = file.readline()
    else:
        link = 'https://www.novels.pl/novel/Super-Gene-Optimization-Fluid-WN6/1/Chapter-1-Xia-Fei.html'

    # link should be to first chapter that should be downloaded

    # link = 'https://www.novels.pl/novel/NSHBA-WN/1_1/Chapter-1-Memories-of-a-Pill-God.html'
    # base_link = 'https://www.novels.pl'
    # directory = "nine-star-hegemon"

    num_chapters = 2
    split = urlsplit(link)

    base_link = split.scheme + '://' + split.netloc
    # print(base_link)
    # print(split.scheme)
    directory = split.path.split('/')[-3]
    # print(directory)

    # TODO gather urls as a list and pass the list to each function to avoid crawling twice

    download_audio(num_chapters, link, base_link, directory)

    # download_text(num_chapters, link, base_link, directory)

    # for filename in os.listdir(directory):
    #     f = os.path.join(directory, filename)
    #     g = os.path.join(output_dir, filename.split('.')[0] + ".mp3")
    #     convert(f, g)
    return


def download_text(num_chapters, link, base_link, directory):
    for _ in range(num_chapters):
        response = requests.get(link)

        # Parse the HTML of the website using Beautiful Soup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Use Beautiful Soup's built-in methods to search for and extract the data you're interested in
        # For example, you could use the find_all() method to find all <p> tags and then extract their text:
        chapter_text = ""
        paragraphs = soup.find('div', class_='panel-body article').find_all('p')
        for p in paragraphs:
            # print(p.text)
            chapter_text += " " + p.text

        with open(os.path.join(directory, (link.split('/')[-1]).split('.')[0] + ".txt"), 'w', encoding='utf-8-sig') as file:
            file.write(chapter_text.encode('ascii', 'ignore').decode('ascii'))

        next_link = soup.find('li', class_='next').a.get('href')
        if next_link:
            link = base_link + next_link
            print(link)
            with open('next_link.txt', 'w') as file:
                file.write(link)
        time.sleep(0.5)



def download_audio(num_chapters, link, base_link, directory):
    if not os.path.exists(directory):
        # Create the directory if it doesn't exist
        os.makedirs(directory)

    for _ in range(num_chapters):
        print(link)

        import requests
        from bs4 import BeautifulSoup

        response = requests.get(link)
        # print(response)

        # Parse the HTML of the website using Beautiful Soup
        soup = BeautifulSoup(response.text, 'html.parser')
        chapter_id = (link.split('/')[-2]) + ".mp3"
        # id = (link.split('/')[-1]).split('.')[0] + ".mp3")
        # Only download if it isn't already there
        if not os.path.exists(os.path.join(directory, chapter_id)):
            # download_link = soup.find('div', class_='col-sm-8 text-left').find('div', class_='panel-body').a.get('href')
            audio_src = soup.find('div', class_='col-sm-8 text-left').find('div', class_='panel-body').find("source")["src"]
            # print(f'base_link: {base_link}\naudio_src: {audio_src}')
            full_audio_url = urljoin(base_link, audio_src)
            # print(f'full_audio_url: {full_audio_url}')
            mp3response = requests.get(full_audio_url)

            with open(os.path.join(directory, chapter_id), 'wb') as f:
                f.write(mp3response.content)
            time.sleep(0.5)

        next_link = soup.find('li', class_='next').a.get('href')
        if next_link:
            link = base_link + next_link
            with open('next_link.txt', 'w') as file:
                file.write(link)


def convert(inputName, outputName):
    print("Converting", inputName)
    language = 'en'
    with open(inputName, 'r') as file:
        myAudio = gTTS(text=file.read(), lang=language, slow=False)
        myAudio.save(outputName)


if __name__ == '__main__':
    main()
