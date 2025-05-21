import os
import requests
from datetime import datetime

SUPABASE_URL = os.environ["SUPABASE_URL"]
SUPABASE_KEY = os.environ["SUPABASE_SERVICE_ROLE_KEY"]
TABLE_NAME = "videos_to_upload"
STORAGE_BUCKET = "videos"

headers = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
}

def get_videos_to_upload():
    today = datetime.utcnow().date().isoformat()
    query_url = f"{SUPABASE_URL}/rest/v1/{TABLE_NAME}?upload_date=eq.{today}&select=*"
    response = requests.get(query_url, headers=headers)
    response.raise_for_status()
    return response.json()

def download_video(file_path):
    file_url = f"{SUPABASE_URL}/storage/v1/object/public/{STORAGE_BUCKET}/{file_path}"
    local_path = file_path.split("/")[-1]
    r = requests.get(file_url, stream=True)
    r.raise_for_status()
    with open(local_path, 'wb') as f:
        for chunk in r.iter_content(chunk_size=8192):
            f.write(chunk)
    print(f"Downloaded {file_url}")
    return local_path

def main():
    videos = get_videos_to_upload()
    print(f"{len(videos)} video(s) scheduled for today.")
    for video in videos:
        video_path = video.get("file_path")  # pl: "uploads/myvideo.mp4"
        if video_path:
            local_file = download_video(video_path)
            # TODO: add your upload logic here (e.g. upload_to_youtube(local_file))
        else:
            print("No file_path found in record.")

if __name__ == "__main__":
    main()
