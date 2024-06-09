import requests as re
import json
import base64
import pyDes
import os
import re as s
from tqdm import tqdm as pro
from bs4 import BeautifulSoup as soup
from mutagen.mp4 import MP4, MP4Cover
from colorama import Fore,Back,Style

def search_and_fetch():
    singer = input("Enter the singer name: ").strip() or "diljit"
    singer = singer.split(',')
    data_list = []
    for singer_name in singer:
        url = f"https://www.jiosaavn.com/api.php?p=1&q={singer_name}&_format=json&_marker=0&api_version=4&ctx=wap6dot0&n=20&__call=search.getResults"
        response = re.get(url)
        data = json.loads(response.text)
        data_list.append(data)
    return data_list

def extraction(data_list):
    for data in data_list:
        for i, result in enumerate(data['results']):
            url_list.append(result['perma_url'])
            image.append(result['image'])
            more_info = result['more_info']
            enc_url.append(more_info['encrypted_media_url'])

            clean_title = s.sub(invalid_char," ", result['title']).split('From')[0].strip('.').strip('_')
            print(i, ': ', clean_title)
            title.append(clean_title)

            artists = [artist['name'] for artist in result['more_info']['artistMap']['primary_artists']]
            artist_list.append(artists)

        download()
        

def download():
    choice = input("Enter choice (x=all): ").strip()
    if choice == 'x':
        choices = range(20)
    else:
        choices = map(int, choice.split())

    for ser in choices:
        with open(f'{title[ser]}.m4a', mode='wb') as fhand:
            url = decrypt_media_url(enc_url[ser])
            url = url.replace('_96.mp4', '_320.mp4')
            song = re.get(url, stream=True)
            progress(song, fhand)
        meta_add(ser)

        print(f"Downloaded {title[ser]}")
    refresh()

def decrypt_media_url(enc_url):
    enc_url = base64.b64decode(enc_url)
    dec_url = encryption.decrypt(enc_url, padmode=pyDes.PAD_PKCS5).decode("utf-8")
    return dec_url

def progress(song, fhand):
    total_size = int(song.headers.get('content-length', 0))
    chunk = 1024
    t = pro(total=total_size, unit="iB", unit_scale=True, colour="green")
    for song_data in song.iter_content(chunk):
        t.update(len(song_data))
        fhand.write(song_data)
    t.close()

def meta_add(ser):
    with open(f'{title[ser]}_high_res.jpg', mode='wb') as ihand:
        img_url = image[ser].replace('150x150.jpg', '500x500.jpg')
        res_img_500 = re.get(img_url)
        ihand.write(res_img_500.content)

    audio = MP4(f'{title[ser]}.m4a')
    with open(f'{title[ser]}_high_res.jpg', 'rb') as img_file:
        img_data = img_file.read()
        cover = MP4Cover(img_data, imageformat=MP4Cover.FORMAT_JPEG)
        audio.tags['covr'] = [cover]
        audio['title'] = title[ser]
        artist = ' '.join(artist_list[ser][:2]) or artist_list[ser][0]
        audio['\xa9ART'] = artist
        audio.save()
    os.remove(f'{title[ser]}_high_res.jpg')

def refresh():
    url_list.clear()
    enc_url.clear()
    title.clear()
    image.clear()
    artist_list.clear()

url_list = []
enc_url = []
title = []
image = []
artist_list = []
invalid_char = r'[<>:"/\\|?*()@$!#%^&;:]'
encryption = pyDes.des(b"38346591", pyDes.ECB, b"\0\0\0\0\0\0\0\0", pad=None, padmode=pyDes.PAD_PKCS5)

print(Fore.BLUE,'Welcome to Saavn')
print(Style.RESET_ALL)
while True:
 extraction(search_and_fetch())
 x=input("Continue(Y|N): ").upper()
 if x!="Y":
     break  
#inclucded for package satisfaction  
def exit():
 print("Visit again")
