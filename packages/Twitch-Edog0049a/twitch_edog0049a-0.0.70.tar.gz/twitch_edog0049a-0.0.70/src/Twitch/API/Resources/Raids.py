from Twitch.API.Resources.__imports import *

class StartaraidRequest(Utils.RequestBaseClass):
    requestType = Utils.HTTPMethod.POST
    scope = Scope.Channel.Manage.Raids
    authorization = Utils.AuthRequired.USER
    endPoint ="/raids"
    def __init__(self, from_broadcaster_id: str, to_broadcaster_id: str) -> None:
        self.from_broadcaster_id = from_broadcaster_id
        self.to_broadcaster_id = to_broadcaster_id
        super().__init__()

class Raid:
    created_at: str
    is_mature: bool

class StartaraidResponse(Utils.ResponseBaseClass):
    def __init__(self) -> None:
        super().__init__(Raid)

class CancelaraidRequest(Utils.RequestBaseClass):
    requestType = Utils.HTTPMethod.DELETE
    scope = Scope.Channel.Manage.Raids
    authorization = Utils.AuthRequired.USER
    endPoint ="/raids"
    def __init__(self, broadcaster_id: str) -> None:
        self.broadcaster_id = broadcaster_id
        super().__init__()
    

class CancelaraidResponse(Utils.ResponseBaseClass):
        def __init__(self) -> None:
            super().__init__(None   )
