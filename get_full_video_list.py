import os
import requests
from bs4 import BeautifulSoup
import csv

# Get a lists of videos with url, name, length, date and up name info from a single page with Beautiful Soup.
def get_url_info_list(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text,'lxml')
    video_links = soup.find_all('div',class_='info')
    video_lengths = soup.find_all('a',class_='img-anchor')
    videos = []
    v_len = []

    for vl in video_links:
        video_date = vl.find('span',class_='so-icon time').text.strip()
        video_title = vl.find('a').get('title')
        video_up = vl.find('a',class_='up-name').text
        up_uid = vl.find('a',class_='up-name').get('href')
        if '?from=search' in up_uid:
            start_index = up_uid.index('.com/')
            end_index = up_uid.index('?from=search')
            up_uid = up_uid[start_index+5:end_index]
        video_url = 'https:'+vl.find('a').get('href')
        if '?from=search' in video_url:
            end_index = video_url.index('?from=search')
            video_url = video_url[:end_index]
        videos.append([video_date,video_title,video_up,up_uid,video_url])

    for vbp in video_lengths:
        video_time = vbp.find('span',class_='so-imgTag_rb').text
        v_len.append(video_time)

    for i in range(len(video_links)):
        videos[i].insert(2,v_len[i])

    return videos

# Scrape from all pages and add non-duplicate entries to one list
def create_list(urls):
    full_list = []
    for url in urls:
        videos = get_url_info_list(url)
        for v in videos:
            if v not in full_list:
                full_list.append(v)
    return full_list

# Create a CSV file with the result video list
def create_csv(video_list, filepath):
    fields = ['video_date','video_title','video_time','video_up','up_uid','video_url']
    rows = video_list

    with open(filepath, 'w') as f:
        write = csv.writer(f)
        write.writerow(fields)
        write.writerows(rows)

# old version website, 20 videos per page, keyword: Billy Sheehan, sorted by release date (website built-in function)
base_url = 'https://search.bilibili.com/all?keyword=Billy%20Sheehan&order=pubdate&duration=0&tids_1=0' 
urls = [base_url+'&page='+str(i+1) for i in range(5)]

print('Retrieve search result for keyword "Billy Sheehan"...')
videos = create_list(urls)
print('List retrieved, '+str(len(videos))+' videos in total.')
print('Create list csv file...')

if not os.path.exists('list'):
    os.makedirs('list')
list_path = os.path.dirname(__file__)+'/list/video_list.csv' # absolute path of video list file
create_csv(videos,list_path)
print('List file created under /list folder.')