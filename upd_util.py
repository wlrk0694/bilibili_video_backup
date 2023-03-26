import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd

# Get a lists of videos with url, name, length, date and uploader info from a single page with Beautiful Soup.
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
        # videos.append([video_date,video_title,video_up,video_url])
        videos.append([video_date,video_title,video_up,up_uid,video_url])

    for vbp in video_lengths:
        video_time = vbp.find('span',class_='so-imgTag_rb').text
        v_len.append(video_time)

    for i in range(len(video_links)):
        videos[i].insert(2,v_len[i])

    return videos

# Scrape from first few pages (depends on updating frequency) and add non-duplicate entries to one list
def create_list(urls):
    new_list = []
    for url in urls:
        resp_len = 0 # setup a parameter to repeat requests until get_url_info_list() method return non-empty list
        while resp_len == 0:
            videos = get_url_info_list(url)
            resp_len = len(videos)
        for v in videos:
            if v not in new_list:
                new_list.append(v)
    return new_list

# Check overlap with existing csv file
def update_list(new,field,filepath):
    old = []
    with open(filepath, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            if 'video_date' not in row:
                old.append(row)
    old_df = pd.DataFrame(old,columns = field)
    new_df = pd.DataFrame(new,columns = field)

    print('Original list length: '+str(old_df.shape[0]))

    merged_df = pd.concat([new_df,old_df]) # Merge new scrape and existing scrape
    merged_df.drop_duplicates(inplace=True,ignore_index = True) # Remove complete duplicates
    
    updated = new_df[~new_df['video_url'].isin(old_df['video_url'])] # new uploads: new url
    updated = updated.reset_index(drop = True)
    modified = merged_df[merged_df.duplicated(subset =['video_url'])] # modified uploads: same url, different video duration
    modified = modified.reset_index(drop = True)

    # final merge, keep latest modified upload
    merged_df.drop_duplicates(subset = ['video_url'],keep='first',inplace=True)
    
    return updated, modified, merged_df