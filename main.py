import os
import requests
import yt_dlp
import aiohttp
import asyncio
from pathlib import Path

# Configuration
FLIC_TOKEN = "flic_da5a13caa14f0cc5c124532ef942f8c9986907e3ed6fe4778cdd1ecf74aec22c"  # Replace with your Flic-Token
CATEGORY_ID = 25  # Replace with the appropriate category ID
VIDEO_PATH = Path("./videos")  # Directory to monitor for new .mp4 files
VIDEO_URLS = ["https://www.instagram.com/reel/C-w2tYiuMLi/"]  # Add Instagram/TikTok URLs here

# Ensure the videos directory exists
VIDEO_PATH.mkdir(parents=True, exist_ok=True)

# Function to download video from Instagram/TikTok
def download_video(url, output_path):
    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',
        'outtmpl': str(output_path),
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

# Function to get the upload URL
def get_upload_url():
    url = "https://api.socialverseapp.com/posts/generate-upload-url"
    headers = {
        "Flic-Token": FLIC_TOKEN,
        "Content-Type": "application/json"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to get upload URL: {response.status_code}")
        return None

# Function to upload video via PUT request
async def upload_video(upload_url, video_path):
    async with aiohttp.ClientSession() as session:
        with open(video_path, 'rb') as video_file:
            async with session.put(upload_url, data=video_file) as response:
                if response.status == 200:
                    print(f"Successfully uploaded {video_path}")
                    return True
                else:
                    print(f"Failed to upload {video_path}: {response.status}")
                    return False

# Function to create a post with the uploaded video
def create_post(title, hash_value):
    url = "https://api.socialverseapp.com/posts"
    headers = {
        "Flic-Token": FLIC_TOKEN,
        "Content-Type": "application/json"
    }
    data = {
        "title":"POWER",
        "hash": hash_value,
        "is_available_in_public_feed": True,
        "category_id": CATEGORY_ID
    }
    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 200:
        print(f"Post created with title: {title}")
    else:
        print(f"Failed to create post: {response.status_code}")

# Function to delete the local video file after upload
def delete_local_video(video_path):
    try:
        os.remove(video_path)
        print(f"Deleted {video_path}")
    except Exception as e:
        print(f"Error deleting file: {e}")

# Function to monitor the videos directory for new files
async def monitor_videos_directory():
    print(f"Monitoring {VIDEO_PATH} for new .mp4 files...")
    processed_files = set()
    while True:
        for file in VIDEO_PATH.glob("*.mp4"):
            if file.name not in processed_files:
                print(f"Processing new video: {file.name}")
                processed_files.add(file.name)
                await process_video(file)
        await asyncio.sleep(5)  # Check every 5 seconds

# Function to handle video download and processing
async def handle_video_download(video_url):
    video_file_path = VIDEO_PATH / f"{os.path.basename(video_url)}.mp4"
    print(f"Downloading video from {video_url}...")
    download_video(video_url, video_file_path)
    print(f"Downloaded video to {video_file_path}")

# Function to handle video processing
async def process_video(video_file):
    # Step 1: Get upload URL
    response = get_upload_url()
    if response is None or 'url' not in response:
        print("Upload URL missing in the response.")
        return

    upload_url = response['url']
    video_hash = response['hash']

    # Step 2: Upload video
    upload_success = await upload_video(upload_url, video_file)

    if upload_success:
        # Step 3: Create post
        video_title = video_file.stem
        create_post(video_title, video_hash)

        # Step 4: Delete local video after upload
        delete_local_video(video_file)

# Main function to start the process
async def main():
    # Start monitoring directory for new videos
    monitor_task = asyncio.create_task(monitor_videos_directory())

    # Download videos from specified URLs
    for url in VIDEO_URLS:
        await handle_video_download(url)

    # Keep the program running for monitoring
    await monitor_task

# Run the program
if __name__ == "__main__":
    asyncio.run(main())
