from Twitch.API.Resources.__imports import *
class GetCreatorGoalsRequest(Utils.RequestBaseClass):
    requestType = Utils.HTTPMethod.GET
    scope = Scope.Channel.Read.Goals
    authorization = Utils.AuthRequired.USER
    endPoint ="/goals"
    def __init__(self, broadcaster_id: str) -> None:
        self.broadcaster_id = broadcaster_id
        super().__init__()
class Goal:
    id: str 
    broadcaster_id: str
    broadcaster_name: str
    broadcaster_login: str
    type: str
    description: str
    current_amount: int
    target_amount: int
    created_at: str
    
class GetCreatorGoalsResponse(Utils.ResponseBaseClass):
    def __init__(self) -> None:
        super().__init__(Goal)
