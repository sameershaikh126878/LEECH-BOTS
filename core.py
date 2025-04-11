import os
import requests
from bs4 import BeautifulSoup
from yt_dlp import YoutubeDL
from tqdm import tqdm

def download_pdf(url, save_path="downloads/"):
    os.makedirs(save_path, exist_ok=True)
    local_filename = url.split("/")[-1].split("?")[0]
    full_path = os.path.join(save_path, local_filename)
    
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        total = int(r.headers.get('content-length', 0))
        with open(full_path, 'wb') as f, tqdm(
            desc=local_filename,
            total=total,
            unit='B',
            unit_scale=True,
            unit_divisor=1024,
        ) as bar:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
                bar.update(len(chunk))
    return full_path

def download_video(video_url, save_path="downloads/"):
    os.makedirs(save_path, exist_ok=True)
    ydl_opts = {
        'outtmpl': os.path.join(save_path, '%(title)s.%(ext)s'),
        'format': 'bestvideo+bestaudio/best',
        'merge_output_format': 'mp4',
        'noplaylist': True,
        'quiet': True,
    }
    with YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(video_url, download=True)
        return ydl.prepare_filename(info_dict)

def extract_links_from_pw_page(pw_url):
    response = requests.get(pw_url)
    soup = BeautifulSoup(response.text, 'lxml')
    links = []
    for a_tag in soup.find_all('a', href=True):
        href = a_tag['href']
        if "pdf" in href.lower() or "m3u8" in href or "drive" in href:
            links.append(href)
    return links
