from Twitch.API.Resources.__imports import *

class SearchCategoriesRequest(Utils.RequestBaseClass):
    requestType = Utils.HTTPMethod.GET
    scope = None
    authorization = Utils.AuthRequired.CLIENT
    endPoint ="/search/categories"
    def __init__(self, query: str, first: Optional[str]=None, after: Optional[str]=None) -> None:
            self.query = query
            self.first = first
            self.after = after
            super().__init__()
    
class Category:
    box_art_url: str
    id: str
    name: str

class SearchCategoriesResponse(Utils.ResponseBaseClass):
    def __init__(self) -> None:
        super().__init__(Category)

class SearchChannelsRequest(Utils.RequestBaseClass):
    requestType = Utils.HTTPMethod.GET
    scope = None
    authorization = Utils.AuthRequired.CLIENT
    endPoint ="/search/channels"
    def __init__(self, query: str, live_only: Optional[bool], first: Optional[str]=None, after: Optional[str]=None) -> None:
        self.query = query
        self.live_only = live_only
        self.first = first
        self.after = after
        super().__init__()

class Channel:
    broadcaster_language: str
    broadcaster_login: str
    display_name: str
    game_id: str
    game_name: str
    id: str
    is_live: bool
    tags: List[str]
    thumbnail_url: str
    title: str
    started_at: str

class SearchChannelsResponse(Utils.ResponseBaseClass):
        def __init__(self) -> None:
            super().__init__(Channel)