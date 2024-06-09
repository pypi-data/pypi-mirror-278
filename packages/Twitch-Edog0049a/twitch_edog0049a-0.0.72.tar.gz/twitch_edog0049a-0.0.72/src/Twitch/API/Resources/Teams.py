from Twitch.API.Resources.__imports import *

class GetChannelTeamsRequest(Utils.RequestBaseClass):
        requestType = Utils.HTTPMethod.GET
        scope = None
        authorization = Utils.AuthRequired.CLIENT
        endPoint ="/teams/channel"
        def __init__(self, broadcaster_id: str, userAuth=False) -> None:
                if userAuth:
                        self.authorization = Utils.AuthRequired.USER
                self.broadcaster_id = broadcaster_id
                super().__init__()

class BroadcasterTeam:
        broadcaster_id: str
        broadcaster_login: str
        broadcaster_name: str
        background_image_url: str
        banner: str
        created_at: str
        updated_at: str
        info: str
        thumbnail_url: str
        team_name: str
        team_display_name: str
        id: str


class GetChannelTeamsResponse(Utils.ResponseBaseClass):
        def __init__(self) -> None:
            super().__init__(BroadcasterTeam)

class GetTeamsRequest(Utils.RequestBaseClass):
        requestType = Utils.HTTPMethod.GET
        scope = None
        authorization = Utils.AuthRequired.CLIENT
        endPoint ="/teams"
        def __init__(self, name: Optional[str]=None, id: Optional[str]=None, userAuth=False) -> None:
                if userAuth:
                        self.authorization = Utils.AuthRequired.USER
                if name == None and id == None:
                        raise ValueError("Either name or id must be provided")
                if name != None and id != None:
                        raise ValueError("Only one of name or id can be provided")
                self.name = name
                self.id = id
                super().__init__()
class User:
        user_id: str
        user_name: str
        user_login: str
       
class Team:
        users: List[User]
        background_image_url: str
        banner: str
        created_at: str
        updated_at: str
        info: str
        thumbnail_url: str
        team_name: str
        team_display_name: str
        id: str    

class GetTeamsResponse(Utils.ResponseBaseClass):
        def __init__(self) -> None:
            super().__init__(Team)