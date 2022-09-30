import os
import cv2
import csv
import shutil

# Download video(s) from bilibili URL (may be incompleted or unable to download due to invalid URL)
def dl_bilibili(filepath,url):
    s = os.system('you-get -o {} --playlist -k "{}"'.format(filepath,url))
    # --playlist command can be used for single video as well   

# Convert names of all XML files in the folder (only existing ones, no danger of error)
def rename_xmls(filepath):
    for file in os.listdir(filepath):
        if os.path.isfile(os.path.join(filepath,file)):
            if '.cmt.xml' in file:
                new_name = file[:len(file)-8] + '.xml'
                print('Changing xml name: ',file,' to ',new_name)
                print('----------------------------------------')
                os.rename(file,new_name)

# Check for multi-part videos (list item may end with '.download' or '.mp4')
def check_multi(filepath):
    video_list = []
    for file in os.listdir(filepath):
        if os.path.isfile(os.path.join(filepath, file)):
            if '.mp4' in file:
                video_list.append(file)
    return video_list
    
# Find single video resolution
def find_resolution(filepath,video_file):
    video_path = filepath+video_file
    vid = cv2.VideoCapture(video_path)
    height = int(vid.get(cv2.CAP_PROP_FRAME_HEIGHT)) # always 0 in Linux python3
    width  = int(vid.get(cv2.CAP_PROP_FRAME_WIDTH))  # always 0 in Linux python3
    return width, height

# Convert single subtitle to ass format (skip the incomplete file or ones missing danmaku file)
def conv_sub(filepath,video_file):
    if '.download' in video_file:
        print('***Warning: Download is not completed, please redownload manually.')
    else:
        [width,height] = find_resolution(filepath,video_file)
        danmaku_name = video_file[:(len(video_file)-4)]
        danmaku_file = danmaku_name +'.xml'
        if os.path.isfile(os.path.join(filepath, danmaku_file)):
            sub_convert = danmaku_name+'.ass'
            print('Converting danmaku...')
            s = os.system('python3 danmaku2ass.py -o "{}" -s {}x{} -fn "MS PGothic" -fs 40 -a 0.6 -dm 10 -ds 5 "{}"'.format(sub_convert,width,height,danmaku_file))
            print('Converting completed.')
            return True
        else:
            print('***Warning: Danmaku file is missing, please redownload manually.')
    return False

# Move all files with same name to another directory (skip incomplete download or missing file)
def move_files(source,destination,video_file,converted):
    if '.download' in video_file:
        print('***Warning: Moving failed, video download is not completed.')
    elif not converted:
        print('***Warning: Moving failed, danmaku file is missing.')
    else:
        video_file_src = source+video_file
        xml_file_src = source+video_file[:len(video_file)-4]+'.xml'
        ass_file_src = source+video_file[:len(video_file)-4]+'.ass'
        video_file_dst = destination+video_file
        xml_file_dst = destination+video_file[:len(video_file)-4]+'.xml'
        ass_file_dst = destination+video_file[:len(video_file)-4]+'.ass'
        print('Moving files...')
        shutil.move(video_file_src,video_file_dst)
        shutil.move(xml_file_src,xml_file_dst)
        shutil.move(ass_file_src,ass_file_dst)

# Create or update list including invalid URLs and exclude invalid URLs from existing list
def update_invalid_csv(invalid_urls,list_path,invalid_path):
    invalid_list = []
    valid_list = []
    try:
        with open(invalid_path, 'r') as f:
            # Retrieve the existing invalid list
            reader = csv.reader(f)
            for row in reader:
                if 'video_date' not in row:
                    invalid_list.append(row)
    except:
        print('Warning: no invalid URL list available')
        print('Creating empty invalid list...')
    else:
        print('')
    finally:        
        with open(list_path, 'r') as f:
            # Search the video list for invalid URLs and move corresponding info to invalid list
            reader = csv.reader(f)
            for row in reader:
                if 'video_date' not in row:
                    if row[4] in invalid_urls:
                        invalid_list.append(row) # add info of invalid URLs to invalid_list
                    else:
                        valid_list.append(row) # exclude invalid URLs from video_list

        fields = ['video_date','video_title','video_time','video_up','video_url']
        inv_rows = invalid_list
        rem_rows = valid_list

        with open(invalid_path, 'w') as f:
            write = csv.writer(f)
            write.writerow(fields)
            write.writerows(inv_rows)

        with open(list_path, 'w') as f:
            write = csv.writer(f)
            write.writerow(fields)
            write.writerows(rem_rows)