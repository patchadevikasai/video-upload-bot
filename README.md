# 🎥 Video Search and Upload Bot Assignment

This project allows to download a video from Instagram upload it to a social media platform using the Flic API, and create a post with the uploaded video. The process involves downloading a video, uploading it to the platform, creating a post with metadata, and deleting the local video file after upload.

## 📋 Requirements

Before running the project, you need to have the following installed:

- Python 3.7+
- 📥`yt-dlp` for downloading videos
- 🌐`aiohttp` for asynchronous HTTP requests
- 🔑`requests` for interacting with the Flic API

You can install the required Python packages using the following command:

```bash
pip install yt-dlp aiohttp requests

```
## ⚙️Setup
1.🔑Replace the FLIC_TOKEN with your actual Flic API token.

2.🗂️ Update the CATEGORY_ID with the appropriate category ID where you want the video to be posted.

3.🎬Replace VIDEO_URL with the Instagram or TikTok video URL you want to download and upload.

## How It Works
1.📥Download Video: The video is downloaded using yt-dlp from the provided Instagram or TikTok URL.

2.⬆️Upload Video: After the video is downloaded, the script retrieves an upload URL from the Flic API and uploads the video.

3.📝Create Post: Once the video is uploaded, a post is created on the platform with the provided title and metadata.

4.🗑️Delete Local Video: After the upload and post creation, the local video file is deleted to save space.

## 🚀Usage
To run the program, simply execute the main.py script:
```
python main.py
```
The script will automatically handle the download, upload, and post creation process.
## 📝License
This project is licensed under the MIT License.
