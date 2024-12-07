Video Downloader and Uploader

This project allows you to download videos from Instagram or TikTok, upload them to a social media platform using the Flic API, and create posts with the uploaded videos. It automates the process of downloading, uploading, posting, and deleting the local video after the process is complete.


📋 Requirements
Before running the project, ensure you have the following installed:
•	🐍 Python 3.7+
•	📥 yt-dlp for downloading videos
•	🌐 aiohttp for asynchronous HTTP requests
•	🔑 requests for interacting with the Flic API

You can install the required Python packages using the following command:
pip install yt-dlp aiohttp requests

⚙️ Setup
1.	🔑 Replace the FLIC_TOKEN with your actual Flic API token.
2.	🗂️ Update the CATEGORY_ID with the appropriate category ID where you want the video to be posted.
3.	🎬 Replace VIDEO_URL with the Instagram or TikTok video URL you want to download and upload.


🔄 How It Works
1.	📥 Download Video: The video is downloaded from Instagram or TikTok using yt-dlp and saved locally.
2.	⬆️ Upload Video: After the video is downloaded, the script retrieves an upload URL from the Flic API and uploads the video.
3.	📝 Create Post: A post is created on the platform with the uploaded video, including the provided metadata such as the title and category.
4.	🗑️ Delete Local Video: After uploading and posting, the local video file is deleted to save disk space.


🚀 Usage
To run the program, simply execute the main.py script:
python main.py
The script performs the following tasks:
•	Downloads the video from the provided URL (VIDEO_URL).
•	Retrieves an upload URL using the Flic API.
•	Uploads the video to the platform.
•	Creates a post with the uploaded video.
•	Deletes the local video file after the upload is complete.

Sample Output:

Downloading video from https://www.instagram.com/p/C41wjYCyvUj/...
Successfully uploaded video.mp4
Post created with title: C41wjYCyvUj
Deleted video.mp4


📂 Project Structure
The project structure is simple:
- main.py            # Main script to download, upload, and post video

📝 License
This project is licensed under the MIT License - see the LICENSE file for details.
________________________________________
Code Explanation:
1.	Configuration Variables:
	a.FLIC_TOKEN: Your Flic API token.
	b.CATEGORY_ID: The category where you want to post the video.
	c.VIDEO_URL: The Instagram/TikTok URL from which you want to download the video.
	d.VIDEO_PATH: The local file path where the video will be saved.

2.	Functions:
   a.download_video(url, output_path): Downloads the video from Instagram or TikTok using yt-dlp.
   b.get_upload_url(): Sends a request to the Flic API to get an upload URL for the video.
   c.upload_video(upload_url, video_path): Asynchronously uploads the video to the Flic platform using the provided URL.
   d.create_post(title, hash_value): Creates a post with the uploaded video using the Flic API.
   e.delete_local_video(video_path): Deletes the local video file after the upload is successful.
   f.handle_video(video_url): Main function that orchestrates the entire process, from downloading the video to   uploading and posting it.

3.	Main Program:
  The asyncio.run(handle_video(VIDEO_URL)) line runs the handle_video function and manages the asynchronous tasks.

