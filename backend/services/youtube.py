import os

from dotenv import load_dotenv
from googleapiclient.discovery import build


load_dotenv()

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

youtube = build(
    "youtube",
    "v3",
    developerKey=YOUTUBE_API_KEY
)


def get_playlist_id(url: str):
    if "list=" not in url:
        raise ValueError("Invalid YouTube playlist URL")

    playlist_id = url.split("list=")[1].split("&")[0]

    return playlist_id


def get_playlist_videos(playlist_id: str):

    videos = []

    next_page_token = None

    while True:

        response = youtube.playlistItems().list(
            part="snippet,contentDetails",
            playlistId=playlist_id,
            maxResults=50,
            pageToken=next_page_token
        ).execute()

        for item in response["items"]:

            videos.append({
                "video_id": item["contentDetails"]["videoId"],
                "title": item["snippet"]["title"]
            })

        next_page_token = response.get("nextPageToken")

        if not next_page_token:
            break

    return videos