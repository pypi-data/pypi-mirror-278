from Twitch.API.Resources.__imports import *

class GetSoundtrackCurrentTrackRequest(Utils.RequestBaseClass):
    requestType = Utils.HTTPMethod.GET
    scope = None
    authorization = Utils.AuthRequired.CLIENT
    endPoint = "/soundtrack/current_track"
    def __init__(self, broadcaster_id: str, userAuth=False) -> None:
        if userAuth:
            self.authorization = Utils.AuthRequired.USER
        self.broadcaster_id = broadcaster_id
        super().__init__()  

class Artist:
    creator_channel_id: str
    id: str
    name: str

class Album:
    id: str
    image_url: str
    name: str 

class Track:
    album: Album 
    artists: List[Artist]
    duration: int
    id: str
    isrc: str
    title: str

class Source:
    id: str
    content_type: str
    title: str
    image_url: str
    soundtrack_url: str
    spotify_url: str

class CurrentTrack:
    track: Track
    source: Source

class GetSoundtrackCurrentTrackResponse(Utils.ResponseBaseClass):
        def __init__(self) -> None:
            super().__init__(CurrentTrack)

class GetSoundtrackPlaylistRequest(Utils.RequestBaseClass):
        requestType = Utils.HTTPMethod.GET
        scope = None
        authorization = Utils.AuthRequired.CLIENT
        endPoint ="/soundtrack/playlist"
        def __init__(self, id: str, first: Optional[int] = None, after: Optional[str] = None, userAuth=False) -> None:
            if userAuth:
                self.authorization = Utils.AuthRequired.USER
            self.id = id
            self.first = first
            self.after = after
            super().__init__()
class PlaylistTrack:
    album: Album 
    artists: List[Artist]
    id: str
    isrc: str
    title: str
    duration: int

class GetSoundtrackPlaylistResponse(Utils.PagenationMixin, Utils.ResponseBaseClass):
        def __init__(self) -> None:
            super().__init__(PlaylistTrack)

class GetSoundtrackPlaylistsRequest(Utils.RequestBaseClass):
    requestType = Utils.HTTPMethod.GET
    scope = None
    authorization = Utils.AuthRequired.CLIENT
    endPoint ="/soundtrack/playlists"
    def __init__(self, id: str, first: Optional[int] = None, after: Optional[str] = None, userAuth=False) -> None:
        if userAuth:
            self.authorization = Utils.AuthRequired.USER
        self.id = id
        self.first = first
        self.after = after
        super().__init__()

class Playlist:
    description: str
    id: str
    image_url: str
    title: str

class GetSoundtrackPlaylistsResponse(Utils.ResponseBaseClass):
        def __init__(self) -> None:
            super().__init__(Playlist)
