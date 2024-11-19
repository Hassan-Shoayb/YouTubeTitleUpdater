import os
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

# Scopes required for accessing the YouTube Data API
SCOPES = ["https://www.googleapis.com/auth/youtube.force-ssl"]

def authenticate_youtube_api():
    """Authenticate the YouTube API and generate token.pickle if necessary."""
    credentials = None
    # Check if token.pickle exists
    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            credentials = pickle.load(token)

    # If credentials are invalid or not available, re-authenticate
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            client_id = os.getenv("GOOGLE_CLIENT_ID")
            client_secret = os.getenv("GOOGLE_CLIENT_SECRET")
            flow = InstalledAppFlow.from_client_config(
                {
                    "installed": {
                        "client_id": client_id,
                        "client_secret": client_secret,
                        "redirect_uris": ["http://localhost"]
                    }
                }, SCOPES
            )
            credentials = flow.run_local_server(port=0)

        # Save the credentials for future use
        with open("token.pickle", "wb") as token:
            pickle.dump(credentials, token)

    print("Authentication successful, token.pickle created!")
    return build("youtube", "v3", credentials=credentials)

def update_video_title(video_id):
    """Update the title of a YouTube video with the current view count."""
    youtube = authenticate_youtube_api()

    # Get video details (including view count)
    video_response = youtube.videos().list(
        part="statistics,snippet",
        id=video_id
    ).execute()

    video_info = video_response["items"][0]
    current_views = int(video_info["statistics"]["viewCount"])

    # Format the title with the current view count
    updated_title = f"This video has {current_views:,} views"

    # Update the video title using the YouTube API
    youtube.videos().update(
        part="snippet",
        body={
            "id": video_id,
            "snippet": {
                "title": updated_title,
                "categoryId": video_info["snippet"]["categoryId"],
                "description": video_info["snippet"]["description"],
                "tags": video_info["snippet"].get("tags", [])
            }
        }
    ).execute()

    print(f"Updated title to: {updated_title}")

# Run the script to update video title every time it is triggered by GitHub Actions
if __name__ == "__main__":
    # Replace with your YouTube video ID
    VIDEO_ID = "eSEXbSaydqI"
    
    # Run the update video title function
    try:
        update_video_title(VIDEO_ID)
        print("Title updated.")
    except Exception as e:
        print(f"An error occurred: {e}")
