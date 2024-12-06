import os
import requests
import yt_dlp
import aiohttp

# Configuration
FLIC_TOKEN = "flic_da5a13caa14f0cc5c124532ef942f8c9986907e3ed6fe4778cdd1ecf74aec22c"  # Replace with your Flic-Token
CATEGORY_ID = 25 # Replace with the appropriate category ID
VIDEO_URL = "https://www.instagram.com/p/C41wjYCyvUj/"  # Replace with your Instagram/TikTok URL
VIDEO_PATH = "video.mp4"  # The local path where the video will be saved

# Function to download video from Instagram/TikTok
def download_video(url, output_path):
    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',
        'outtmpl': output_path,
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
        "title":"Mindset_is_everything",
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

# Main function to handle video processing
async def handle_video(video_url):
    # Step 1: Download video
    print(f"Downloading video from {video_url}...")
    download_video(video_url, VIDEO_PATH)

    # Step 2: Get upload URL
    response = get_upload_url()
    if response is None or 'url' not in response:
        print("Upload URL missing in the response.")
        return

    upload_url = response['url']
    video_hash = response['hash']

    # Step 3: Upload video
    upload_success = await upload_video(upload_url, VIDEO_PATH)

    if upload_success:
        # Step 4: Create post
        video_title = os.path.basename(video_url)
        create_post(video_title, video_hash)

        # Step 5: Delete local video after upload
        delete_local_video(VIDEO_PATH)

# Run the video processing
if __name__ == "__main__":
    import asyncio
    asyncio.run(handle_video(VIDEO_URL))
