import os
import asyncio
import requests
import aiohttp
from yt_dlp import YoutubeDL
import subprocess
from pathlib import Path
from dotenv import load_dotenv
import re

# Load environment variables
load_dotenv()

# Constants
VIDEO_DIRECTORY = "videos"
VIDEO_EXT = ".mp4"
FLIC_TOKEN = "flic_da5a13caa14f0cc5c124532ef942f8c9986907e3ed6fe4778cdd1ecf74aec22c"  # Your token from Empowerverse API
UPLOAD_URL_ENDPOINT = "https://api.socialverseapp.com/posts/generate-upload-url"
UPLOAD_VIDEO_ENDPOINT = "https://dl.app.socialverseapp.com/"
CATEGORY_ID = 1  # Adjust based on your requirement
Path(VIDEO_DIRECTORY).mkdir(parents=True, exist_ok=True)

# Check if ffmpeg is available
def check_ffmpeg():
    try:
        subprocess.run([r'C:\Program Files\ffmpeg-7.1-full_build\bin\ffmpeg.exe', '-version'], check=True)
        print("FFmpeg is installed and available.")
    except FileNotFoundError:
        print("FFmpeg not found. Please ensure FFmpeg is installed and the path is correct.")
        exit(1)
    except subprocess.CalledProcessError:
        print("Error running FFmpeg.")
        exit(1)

# Function to download video from URL (YouTube, Instagram, etc.)
async def download_video(url: str, output_path: str):
    print(f"Downloading video from {url} to {output_path}")  # Debugging output

    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',
        'ffmpeg_location': r'C:\Program Files\ffmpeg-7.1-full_build\bin\ffmpeg.exe',  # Adjust the path
        'noplaylist': True,
        'outtmpl': output_path,  # Specify output path for downloaded video
    }

    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

# Function to get the upload URL from the API
async def get_upload_url():
    headers = {
        "Flic-Token": FLIC_TOKEN,
        "Content-Type": "application/json",
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(UPLOAD_URL_ENDPOINT, headers=headers) as response:
            if response.status == 200:
                data = await response.json()
                return data.get("upload_url")
            else:
                raise Exception(f"Failed to get upload URL: {response.status}")

# Function to upload video to the server using the pre-signed URL
async def upload_video(upload_url: str, video_path: str):
    headers = {
        "Flic-Token": FLIC_TOKEN,
        "Content-Type": "application/json",
    }

    with open(video_path, "rb") as video_file:
        async with aiohttp.ClientSession() as session:
            async with session.put(upload_url, headers=headers, data=video_file) as response:
                if response.status == 200:
                    print(f"Video {video_path} uploaded successfully.")
                    data = await response.json()
                    return data.get("hash")  # Ensure this is the correct field for the hash
                else:
                    raise Exception(f"Failed to upload video: {response.status}")

# Function to create a post with the uploaded video
async def create_post(title: str, video_hash: str):
    if not video_hash:
        raise ValueError("Video hash cannot be None or empty")
    
    headers = {
        "Flic-Token": FLIC_TOKEN,
        "Content-Type": "application/json",
    }

    data = {
        "title": title,
        "hash": video_hash,
        "is_available_in_public_feed": False,
        "category_id": CATEGORY_ID,
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(UPLOAD_VIDEO_ENDPOINT, headers=headers, json=data) as response:
            if response.status == 200:
                print("Post created successfully.")
            else:
                raise Exception(f"Failed to create post: {response.status}")

# Function to extract video name from YouTube URL
def extract_video_name_from_youtube(url: str):
    match = re.search(r"v=([a-zA-Z0-9_-]+)", url)
    if match:
        video_name = match.group(1)
        return video_name  # Don't append .mp4 here
    else:
        raise ValueError("Invalid YouTube URL")

# Function to extract video name from Instagram URL
def extract_video_name_from_instagram(url: str):
    match = re.search(r"instagram\.com/p/([^/]+)/", url)
    if match:
        video_name = match.group(1)
        return video_name  # Don't append .mp4 here
    else:
        raise ValueError("Invalid Instagram URL")

# Function to sanitize the video name
def sanitize_filename(filename: str):
    # Replace invalid characters with underscores
    return re.sub(r'[\\/*?:"<>|]', "_", filename)

# Function to initiate video download and processing
async def initiate_download(url: str):
    # Extract video name based on platform (YouTube or Instagram)
    if "youtube.com" in url:
        video_name = extract_video_name_from_youtube(url)
    elif "instagram.com" in url:
        video_name = extract_video_name_from_instagram(url)
    else:
        raise ValueError(f"Unsupported platform for URL: {url}")

    # Sanitize the video name to remove invalid characters
    sanitized_video_name = sanitize_filename(video_name)

    print(f"Sanitized video name: '{sanitized_video_name}'")  # Debugging output

    # Construct the full video path in the directory
    video_path = os.path.join(VIDEO_DIRECTORY, sanitized_video_name + VIDEO_EXT)  # Append .mp4 here
    print(f"Constructed video path: '{video_path}'")  # Debugging output

    # Ensure the video path is valid
    if not isinstance(video_path, str) or not video_path:
        raise ValueError("Invalid video path: Should be a non-empty string.")

    print(f"Downloading video: '{sanitized_video_name}' to '{video_path}'")  # Debugging output

    # Download the video using the download_video function
    await download_video(url, video_path)

    print(f"Video '{sanitized_video_name}' downloaded successfully.")

# Function to process videos in the directory
async def process_videos():
    while True:
        # Monitor for new videos in the directory
        video_files = [f for f in os.listdir(VIDEO_DIRECTORY) if f.endswith(VIDEO_EXT)]
        
        for video_file in video_files:
            video_path = os.path.join(VIDEO_DIRECTORY, video_file)
            try:
                # Get upload URL
                upload_url = await get_upload_url()

                # Upload the video
                video_hash = await upload_video(upload_url, video_path)

                if video_hash:  # Check if the video hash was returned successfully
                    # Create post after successful upload
                    await create_post(video_file, video_hash)
                
                # Delete the local video file after upload
                os.remove(video_path)

            except Exception as e:
                print(f"Error processing {video_file}: {e}")

        await asyncio.sleep(10)  # Check every 10 seconds

async def main():
    # Ensure FFmpeg is available
    check_ffmpeg()

    # Example URLs (replace with actual URLs)
    video_urls = [
        "https://www.youtube.com/watch?v=Cg7Ii00MVm8",  # YouTube video
        "https://www.instagram.com/p/DDOn4KIvx9x/",  # Instagram post
    ]

    # Download all videos concurrently
    download_tasks = [initiate_download(url) for url in video_urls]
    await asyncio.gather(*download_tasks)

    # Start processing uploaded videos
    await process_videos()

if __name__ == "__main__":
    asyncio.run(main())
