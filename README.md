# bilibili_video_backup
A small project to download videos and subtitles from bilibili


## What is it?
This is a small python project to create a csv file to log existing videos and batch download them from bilibili.com search results based on certain keyword and filter.

WARNING: This project is strictly for personal backup usage. Please do not redistribute any video without the permission from original uploader!

## How to use it?

First you need to install a few Python modules and small tool on your local machine.

- Requests module (Please refer to [documentation](https://pypi.org/project/requests/) for further information)
- bs4 module (Please refer to [documentation](https://pypi.org/project/beautifulsoup4/) for further information)
- cv2 module (Please refer to [documentation](https://pypi.org/project/opencv-python/) for further information)
- [you-get](https://github.com/soimort/you-get) from GitHub, please install via brew (MacOS) or spool
- [danmaku2ass](https://github.com/m13253/danmaku2ass) from [m13253](https://github.com/m13253)


### Contents

This project consists of 5 scripts:
#### 1. get_full_video_list
Get a list of search result (maximum 50 pages) and create a csv file to save the video list info. One piece of video info consists of uploading date, video title, video duration, video uploader, uid, video URL

#### 2. update_list_from_web (module)
Update your existing scraping results and update the list csv file
Caution: This script should only be used after you have executed get_full_video_list.py and retrieved the video list csv file.

#### 3. single_conversion
Download the video from given URL(s), convert all XMLs downloaded by you-get to ass format using Danmaku2Ass. Eventually completed downloads will be moved to file/ folder in the root directory.
Can be used for either batch download or single download. Input should be a single URL or a list of URLs.

#### 4. danmaku2ass
Convert XML downloaded by [you-get](https://github.com/soimort/you-get) from GitHub and convert it to ass format. Please refer to [danmaku2ass](https://github.com/m13253/danmaku2ass) github page for further information.

#### 5. main
Include non-function part from update_list_from_web module, run main.py will get same result as old-version update_list_from_web script and single_conversion script

## Existing issues
- Modified videos need pulling manually
