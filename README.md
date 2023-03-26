# bilibili_video_backup
A small project to download videos and subtitles from bilibili


## What is it?
This is a small python project to create a csv file to log existing videos and batch download them from bilibili.com search results based on certain keyword and filter.

WARNING: This project is strictly for personal backup usage. Please do not redistribute any video without the permission from original uploader!

## How to use it?

First you need to install a few Python modules and small tool on your local machine.

Please run "pip install -r requirements.txt" to install the following module at first
- Requests
- pandas
- beautifulsoup4
- opencv-python
- you-get

Then 
- install [ffmpeg](https://ffmpeg.org/download.html) via brew (MacOS) or tar (WinOS)
- download the python script from [danmaku2ass](https://github.com/m13253/danmaku2ass) from [m13253](https://github.com/m13253) and put in the same folder as other files


### Contents

This project consists of 5 scripts:
#### 1. get_full_video_list
Get a list of search result (maximum 50 pages) and create a csv file to save the video list info. One piece of video info consists of uploading date, video title, video duration, video uploader, uid, video URL

#### 2. upd_util (module)
Update your existing scraping results and update the list csv file
Caution: This script should only be used after you have executed get_full_video_list.py and retrieved the video list csv file.

#### 3. dl_util (module)
Download the video from given URL(s), convert all XMLs downloaded by you-get to ass format using Danmaku2Ass. Eventually completed downloads will be moved to file/ folder in the root directory.
Can be used for either batch download or single download. Input should be a single URL or a list of URLs.

#### 4. danmaku2ass
Convert XML downloaded by [you-get](https://github.com/soimort/you-get) from GitHub and convert it to ass format. Please refer to [danmaku2ass](https://github.com/m13253/danmaku2ass) github page for further information.

#### 5. main
Include non-function part from upd_util and dl_util module

## Existing issues 
- For non-user or users without subscription on bilibili, the highest quality of downloaded videos is limited. It's suggested that you use an account with subscription if possible. For usage, please refer to "Load Cookies" session in [you-get official website](https://you-get.org/).
- When unfinished downloads exist in folder, your later download process will always display moving failed warning.

## Updates
2023-03-26 Add a new parameter and loop to avoid empty response in upd_util module. Will replace with better approach to avoid reCAPTCHA once possible.