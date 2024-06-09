from Twitch.API.Resources.__imports import *

class GetStreamKeyRequest(Utils.RequestBaseClass):
    requestType = Utils.HTTPMethod.GET
    scope = Scope.Channel.Read.Stream_key
    authorization = Utils.AuthRequired.USER
    endPoint ="/streams/key"
    def __init__(self, broadcaster_id: str) -> None:
            self.broadcaster_id = broadcaster_id
            super().__init__()
            
class StreamKey:    
    stream_key: str

class GetStreamKeyResponse(Utils.ResponseBaseClass):
        def __init__(self) -> None:
            super().__init__(StreamKey)

class GetStreamsRequest(Utils.RequestBaseClass):
        requestType = Utils.HTTPMethod.GET
        scope = None
        authorization = Utils.AuthRequired.CLIENT
        endPoint ="/streams"
        def __init__(self, user_id: Optional[List[str]]=None, user_login: Optional[List[str]]=None, 
                     game_id: Optional[List[str]]=None, type: Optional[str]=None, 
                     language: Optional[str]=None, before: Optional[str]=None, 
                     after: Optional[str]=None, first: Optional[str]=None, userAuth=False) -> None:
                
                if userAuth:
                       self.authorization = Utils.AuthRequired.USER

                self.user_id = user_id
                self.user_login = user_login
                self.game_id = game_id
                self.type = type
                self.language = language
                self.before = before
                self.after = after
                self.first = first
                super().__init__()
class Stream:
      id: str
      user_id: str
      user_name: str
      user_login: str
      game_id: str
      game_name: str
      type: str
      title: str
      tags: List[str]
      viewer_count: int
      started_at: str
      language: str
      thumbnail_url: str
      tag_ids: List[str]
      is_mature: bool          

class GetStreamsResponse(Utils.PagenationMixin, Utils.ResponseBaseClass):
        def __init__(self) -> None:
            super().__init__(Stream)

class GetFollowedStreamsRequest(Utils.RequestBaseClass):
        requestType = Utils.HTTPMethod.GET
        scope = Scope.User.Read.Follows
        authorization = Utils.AuthRequired.USER
        endPoint ="/streams/followed"
        def __init__(self, user_id: str, after: Optional[str] = None, first: Optional[str] = None) -> None:
                self.user_id = user_id
                self.after = after
                self.first = first
                super().__init__()
                
class GetFollowedStreamsResponse(Utils.PagenationMixin, Utils.ResponseBaseClass):
        def __init__(self) -> None:
            super().__init__(Stream)

class CreateStreamMarkerRequest(Utils.RequestBaseClass):
        requestType = Utils.HTTPMethod.POST
        scope = Scope.Channel.Manage.Broadcast
        authorization = Utils.AuthRequired.USER
        endPoint ="/streams/markers"
        def __init__(self, user_id: str, description: Optional[str] = None) -> None:
                self.user_id = user_id
                self.description = description
                super().__init__()

class StreamMarker:
        id: str
        created_at: str
        description: str
        position_seconds: int
        url: str
    

class CreateStreamMarkerResponse(Utils.ResponseBaseClass):
        def __init__(self) -> None:
            super().__init__(StreamMarker)

class GetStreamMarkersRequest(Utils.RequestBaseClass):
        requestType = Utils.HTTPMethod.POST
        scope = [Scope.Channel.Manage.Broadcast, Scope.User.Read.Broadcast]
        authorization = Utils.AuthRequired.USER
        endPoint ="/streams/markers"
        def __init__(self, user_id: Optional[str], video_id: Optional[str] = None, after: Optional[str] = None, before: Optional[str] = None, first: Optional[str] = None) -> None:
                self.user_id = user_id
                self.video_id = video_id
                self.after = after
                self.before = before
                self.first = first
                super().__init__()
class Video:
       video_id: str
       markers: List[StreamMarker]

class Mark:
        user_id: str
        user_name: str
        user_login: str
        videos: List[Video]

class GetStreamMarkersResponse(Utils.PagenationMixin, Utils.ResponseBaseClass):
        def __init__(self) -> None:
            super().__init__(Mark)
