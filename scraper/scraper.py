import requests
import time
import re

from bs4 import BeautifulSoup
from tqdm import tqdm

def clean_html_tags(s):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', str(s))
    
    return '\n'+cleantext

# specify lyric's urls
URL = ['https://genius.com/albums/Izone/Color-iz',
       'https://genius.com/albums/Izone/Heart-iz',
       'https://genius.com/albums/Izone/Vampire',
       'https://genius.com/albums/Izone/Bloom-iz',
       'https://genius.com/albums/Izone/Oneiric-diary'] # let's start with these urls

TIMEOUT = 20 # set timeout before each request
LYRIC_PATH = '../data/lyrics.txt'

for u in URL:
    print('Waiting for', TIMEOUT, 'seconds before the next album...')
    time.sleep(TIMEOUT)
    print('Current album:', u)
    
    req = requests.get(u) # initiate GET request to the url
    soup = BeautifulSoup(req.text, 'lxml') # use BeautifulSoup to find the html tags
    
    raw_url = []
    for s in soup.find_all('div'):
        link = s.find('a')
        if link is not None:
            raw_url.append(link.attrs['href'])
            
    songs = []
    for r in raw_url:
        x = re.search('^(http|https)://.*Izone-.*lyrics$', r)
        if x is not None:
            songs.append(r)
            
    non_duplicate_songs = []
    for s in songs:
        if s not in non_duplicate_songs:
            non_duplicate_songs.append(s)
            
    for n in non_duplicate_songs:
        print('Waiting for', TIMEOUT, 'seconds before writing the next song...')
        time.sleep(TIMEOUT)
        
        print('Writing lyrics:', n)
        req = requests.get(n)
        soup = BeautifulSoup(req.text, 'lxml')
        lyrics = []
        for a in tqdm(soup.find_all('div')):
            lyric = a.find('p')
            if lyric is not None:
                lyrics.append(lyric)
    
        lyrics = clean_html_tags(lyrics[0])
        with open(LYRIC_PATH, 'a', encoding='utf-8') as f:
            f.write(lyrics)
            