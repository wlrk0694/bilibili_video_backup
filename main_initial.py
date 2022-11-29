import os
import csv
import pandas as pd
import dl_util as dl
import upd_util as upd

## Initial download from first scrape
list_path = os.path.dirname(__file__)+'/list/video_list.csv'
if not os.path.exists('file'):
    os.makedirs('file')

new = []
with open(list_path, 'r') as f:
    reader = csv.reader(f)
    for row in reader:
        if 'video_date' not in row:
            new.append(row)
fields = ['video_date','video_title','video_time','video_up','up_uid','video_url']
new_df = pd.DataFrame(new,columns = fields)

print(str(new_df.shape[0])+ ' videos have been found from initial scrape.')

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
for i in range(new_df.shape[0]):
    url = new_df.loc[i,"video_url"]
    print('')
    print('Downloading',str(i+1),'out of',str(new_df.shape[0]),' videos...')
    dl.dl_bilibili(source,url)
    dl.rename_xmls(source)
    videos = dl.check_multi(source)
    if len(videos) == 0:
        df1 = pd.DataFrame([list(new_df.loc[i])],columns=fields)
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