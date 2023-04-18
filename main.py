import os
import csv
import pandas as pd
import dl_util as dl
import upd_util as upd

## Update video list, get new and modified video uploads
list_path = os.path.dirname(__file__)+'/list/video_list.csv'
if not os.path.exists('file'):
    os.makedirs('file') # Create video file folder if non-exist

# old version website, 20 videos per page, keyword: Billy Sheehan, sorted by release date (website built-in function)
base_url = 'https://search.bilibili.com/all?keyword=Billy%20Sheehan&order=pubdate&duration=0&tids_1=0'
urls = [base_url+'&page='+str(i+1) for i in range(2)]

new = upd.create_list(urls)

print('')
print('Scraped '+str(len(new)) + ' videos during this session.')

fields = ['video_date','video_title','video_time','video_up','up_uid','video_url']
[updated,modified,merged] = upd.update_list(new,fields,list_path)

print(str(updated.shape[0]+modified.shape[0])+ ' new videos have been released since last scraping.')
if updated.shape[0]+modified.shape[0] != 0:
    print('New list length: '+str(merged.shape[0]))

if updated.shape[0] != 0:
    print('New videos since last scrape:')
    for i in range(updated.shape[0]):
        print(updated.loc[i,"video_url"])

print()
if modified.shape[0] != 0:
    print('Updated videos since last scrape:')
    for i in range(modified.shape[0]):
        print(str(i+1)+'.'+modified.loc[i,"video_title"]+', '+modified.loc[i,"video_url"])

merged.to_csv(list_path,index = False)

source = os.path.dirname(__file__)+'/'
destination = os.path.dirname(__file__)+'/file/'
invalid_path = os.path.dirname(__file__)+'/list/invalid_list.csv'

# read invalid csv into dataframe
invalid = [] # Create an empty list for invalid URLs
if os.path.exists(invalid_path):
    with open(invalid_path, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            if 'video_date' not in row:
                invalid.append(row)
    invalid_df = pd.DataFrame(invalid,columns = fields)
else:
    invalid_df = pd.DataFrame(columns = fields)

# batch download videos - new downloads
for i in range(updated.shape[0]):
    url = updated.loc[i,"video_url"]
    print('')
    print('Downloading',str(i+1),'out of',str(updated.shape[0]),' videos...')
    dl.dl_bilibili(source,url)
    dl.rename_xmls(source)
    videos = dl.check_multi(source)
    if len(videos) == 0:
        df1 = pd.DataFrame([updated.loc[i].to_list()],columns=fields)
        invalid_df = pd.concat([invalid_df,df1])
    elif len(videos) == 1:
        converted = dl.conv_sub(source,videos[0])
        dl.move_files(source,destination,videos[0],converted)
    else:
        converted = []
        for v in videos:
            conv = dl.conv_sub(source,v)
            converted.append(conv)
        if 'False' in converted:
            print('***Warning: Moving failed, video download is not completed.')
        else:
            for v in videos:
                converted = dl.conv_sub(source,v)
                dl.move_files(source,destination,v,converted)

# Download videos out of modified list
if modified.shape[0] != 0:
    print('Start downloading modified ones...')
    for i in range(modified.shape[0]):
        url = modified.loc[i,"video_url"]
        print('')
        print('Downloading',str(i+1),'out of',str(modified.shape[0]),' videos...')
        dl.dl_bilibili(source,url)
        dl.rename_xmls(source)
        videos = dl.check_multi(source)
        if len(videos) == 0:
            df1 = pd.DataFrame([modified.loc[i].to_list()],columns=fields)
            invalid_df = pd.concat([invalid_df,df1])
        elif len(videos) == 1:
            converted = dl.conv_sub(source,videos[0])
            dl.move_files(source,destination,videos[0],converted)
        else:
            converted = []
            for v in videos:
                conv = dl.conv_sub(source,v)
                converted.append(conv)
            if 'False' in converted:
                print('***Warning: Moving failed, video download is not completed.')
            else:
                for v in videos:
                    converted = dl.conv_sub(source,v)
                    dl.move_files(source,destination,v,converted)

if len(invalid) != 0:
    invalid_df.to_csv('invalid_list.csv',index = False)
print('')
print('Downloading and moving completed.')