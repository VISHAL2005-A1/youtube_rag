from pydantic import BaseModel

class PlaylistRequest(BaseModel):
    playlist_url: str