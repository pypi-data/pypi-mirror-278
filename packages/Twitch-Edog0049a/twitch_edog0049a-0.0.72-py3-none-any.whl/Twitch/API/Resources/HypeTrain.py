from Twitch.API.Resources.__imports import *

class GetHypeTrainEventsRequest(Utils.RequestBaseClass):
    requestType = Utils.HTTPMethod.GET
    scope = Scope.Channel.Read.Hype_train
    authorization = Utils.AuthRequired.USER
    endPoint ="/hypetrain/events"
    def __init__(self, broadcaster_id: str, first: Optional[int]=None, after: Optional[str]=None) -> None:
        self.broadcaster_id = broadcaster_id
        self.first = first
        self.after = after
        super().__init__()

class Contribution:
    total: int
    type: str
    user: str


class Event:
    broadcaster_id: str
    cooldown_ends_time: str
    expires_at: str
    goal: int
    id: str
    last_contribution: Contribution
    level: int
    started_at: str
    top_contributions: List[Contribution]
    total: int

class HypeTrainEvent:
    id: str
    event_type: str
    event_timestamp: str
    version: str
    event_data: Event
    

class GetHypeTrainEventsResponse(Utils.PagenationMixin, Utils.ResponseBaseClass):
    def __init__(self) -> None:
        super().__init__(HypeTrainEvent)