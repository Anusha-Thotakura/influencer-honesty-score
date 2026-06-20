"""
src/youtube_collector.py — Collect YouTube influencer data using YouTube Data API v3
HOW TO GET YOUR API KEY:
  1. Go to console.cloud.google.com
  2. Create a new project
  3. Go to APIs & Services → Enable APIs → search "YouTube Data API v3" → Enable
  4. Go to APIs & Services → Credentials → Create Credentials → API Key
  5. Copy that key and paste it below
"""

import requests
import pandas as pd
import time

API_KEY = "PASTE_YOUR_API_KEY_HERE"   # ← replace this

# List of YouTube channel IDs to analyze (fitness channels)
# To find a channel ID: go to the channel page → right click → View Source → search "channelId"
CHANNEL_IDS = [
    "UCVjlpEjEY9GpksqbEesJnNA",  # Example: Fit Tuber
    "UCwnFnYCJiCYCBFGGBWkQxTQ",  # Example: Guru Mann Fitness
    # Add more channel IDs here...
]

def get_channel_stats(channel_id):
    """Fetch stats for one YouTube channel."""
    url = "https://www.googleapis.com/youtube/v3/channels"
    params = {
        "part": "statistics,snippet",
        "id": channel_id,
        "key": API_KEY
    }
    response = requests.get(url, params=params)
    data = response.json()

    if not data.get("items"):
        print(f"  No data for channel {channel_id}")
        return None

    item = data["items"][0]
    stats = item["statistics"]
    snippet = item["snippet"]

    return {
        "username": snippet["title"],
        "channel_id": channel_id,
        "platform": "YouTube",
        "followers": int(stats.get("subscriberCount", 0)),
        "total_posts": int(stats.get("videoCount", 0)),
        "total_views": int(stats.get("viewCount", 0)),
        "avg_views": int(stats.get("viewCount", 0)) // max(int(stats.get("videoCount", 1)), 1),
        "verified": "yes" if snippet.get("localized") else "no",
        "niche": "fitness"
    }

def get_recent_video_stats(channel_id, max_videos=10):
    """Get average likes and comments from the last N videos."""
    # Step 1: Get upload playlist ID
    url = "https://www.googleapis.com/youtube/v3/channels"
    params = {"part": "contentDetails", "id": channel_id, "key": API_KEY}
    res = requests.get(url, params=params).json()

    if not res.get("items"):
        return 0, 0

    playlist_id = res["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]

    # Step 2: Get recent video IDs from that playlist
    url2 = "https://www.googleapis.com/youtube/v3/playlistItems"
    params2 = {"part": "contentDetails", "playlistId": playlist_id, "maxResults": max_videos, "key": API_KEY}
    res2 = requests.get(url2, params=params2).json()

    video_ids = [item["contentDetails"]["videoId"] for item in res2.get("items", [])]
    if not video_ids:
        return 0, 0

    # Step 3: Get likes and comments for those videos
    url3 = "https://www.googleapis.com/youtube/v3/videos"
    params3 = {"part": "statistics", "id": ",".join(video_ids), "key": API_KEY}
    res3 = requests.get(url3, params=params3).json()

    likes_list, comments_list = [], []
    for item in res3.get("items", []):
        s = item["statistics"]
        likes_list.append(int(s.get("likeCount", 0)))
        comments_list.append(int(s.get("commentCount", 0)))

    avg_likes = sum(likes_list) // len(likes_list) if likes_list else 0
    avg_comments = sum(comments_list) // len(comments_list) if comments_list else 0
    return avg_likes, avg_comments


def collect_all():
    results = []
    for channel_id in CHANNEL_IDS:
        print(f"Fetching: {channel_id} ...")
        stats = get_channel_stats(channel_id)
        if stats:
            avg_likes, avg_comments = get_recent_video_stats(channel_id)
            stats["avg_likes"] = avg_likes
            stats["avg_comments"] = avg_comments
            stats["following"] = 0        # YouTube has no following concept
            stats["hypeauditor_score"] = 50  # fill manually later
            results.append(stats)
            print(f"  Done: {stats['username']} — {stats['followers']} subscribers")
        time.sleep(0.5)  # be polite to the API

    df = pd.DataFrame(results)
    df.to_csv("data/raw/influencers_raw.csv", index=False)
    print(f"\nSaved {len(df)} channels to data/raw/influencers_raw.csv")


if __name__ == "__main__":
    collect_all()
