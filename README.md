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

2.🗂️ Update the CATEGORY_ID with the appropriate category ID where you want the video to be posted.

3.🎬Replace VIDEO_URL with the Instagram or TikTok video URL you want to download and upload.

## 💡How It Works
📥 Download Video:
The script downloads the video from the provided Instagram or TikTok URL using yt-dlp.

⬆️ Upload Video:
The downloaded video is uploaded to the Empowerverse Superfeed platform. The script uses the Flic API to obtain an upload URL and completes the upload.

📝 Create Post:
After a successful upload, the script creates a post on the platform with the provided title and metadata.

🗑️ Delete Local Video:
Once the upload and post creation are complete, the local video file is deleted to conserve storage.

## 🚀Usage
To run the program, simply execute the main.py script:
```
python main.py
```
The script will automatically handle the download, upload, and post creation process.

## 📝License
This project is licensed under the MIT License. 
