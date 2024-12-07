# 🎥 Video Search and Upload Bot Assignment

This project empowers users to download a video from Instagram or TikTok, upload it to the Empowerverse Superfeed using the Flic API, and create a post with the uploaded video. The process involves downloading the video, uploading it to the platform, creating a post with metadata, and cleaning up the local video file post-upload.

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

2.🗂️ Replace CATEGORY_ID with the appropriate category ID where you want the video to be posted in the Empowerverse Superfeed.
.

3.🎬Replace VIDEO_URL with the Instagram or TikTok video URL you want to download and upload.

## How It Works
1.📥Download Video: The video is downloaded using yt-dlp from the provided Instagram or TikTok URL.

2.⬆️Upload Video: The downloaded video is uploaded to the Empowerverse Superfeed platform. The script uses the Flic API to obtain an upload URL and completes the upload.

3.📝Create Post: Once the video is uploaded, a post is created on the platform with the provided title and metadata.

4.🗑️Delete Local Video: After the upload and post creation, the local video file is deleted to save space.

## 🚀Usage
To run the program, simply execute the main.py script:
```
python main.py
```
The script will automatically handle the download, upload, and post creation process.

## 📱How to Check Your Uploaded Videos on Empowerverse
1.Download the Empowerverse App:
  - Available for both Android and iOS platforms.

2.Navigate to "Super Feed" Category:

  - Open the app.
  - Go to the Super Feed category.
    
3.Browse Uploaded Videos:

  - Hold the category and click Browse.
  - Check your uploaded videos under this section.

## 📝License
This project is licensed under the MIT License.
Proudly designed to enhance workflows on the Empowerverse Superfeed.
