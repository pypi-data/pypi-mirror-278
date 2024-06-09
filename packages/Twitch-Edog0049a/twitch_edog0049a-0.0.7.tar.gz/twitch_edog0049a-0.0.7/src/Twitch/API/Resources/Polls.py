
from Twitch.API.Resources.__imports import *

class GetPollsRequest(Utils.RequestBaseClass):
    requestType = Utils.HTTPMethod.GET
    scope = Scope.Channel.Read.Polls
    authorization = Utils.AuthRequired.USER
    endPoint = "/polls"
    def __init__(self, broadcaster_id: str, id: Optional[str] = None, first: Optional[str]=None, after: Optional[str]=None) -> None:
        super().__init__()
        self.broadcaster_id = broadcaster_id
        self.id = id
        self.first = first
        self.after = after

class Choices:
    id: str
    title: str
    votes: int
    channel_points_votes: int
    bits_votes: int


class PollsItem:
    id: str
    broadcaster_id: str
    broadcaster_name: str
    broadcaster_login: str
    title: str
    choices: Choices
    bits_voting_enabled: bool
    bit_per_vote: int
    channel_points_voting_enabled: bool
    channel_points_per_vote: int
    status: str
    duration: int
    started_at: str
    ended_at: str

    
class GetPollsResponse(Utils.PagenationMixin, Utils.ResponseBaseClass):
    def __init__(self) -> None:
        super().__init__(PollsItem)

Title: TypeAlias = str
class CreatePollRequest(Utils.RequestBaseClass):
    requestType = Utils.HTTPMethod.POST
    scope = Scope.Channel.Manage.Polls
    authorization = Utils.AuthRequired.USER
    endPoint ="/polls"

    def __init__(self, broadcaste_id: str, title: str, 
                 choices: List[Title], duration: int, 
                 channel_points_voting_enabled: Optional[bool]=None, 
                 channel_points_per_vote: Optional[int]=None) -> None:
        self.broadcaster_id = broadcaste_id
        self.title = title
        self.choices = choices
        self.duration = duration
        self.channel_points_voting_enabled = channel_points_voting_enabled
        self.channel_points_per_vote = channel_points_per_vote
        super().__init__()

class CreatePollResponse(Utils.ResponseBaseClass):
    def __init__(self) -> None:
        super().__init__(PollsItem)

class EndPollRequest(Utils.RequestBaseClass):
    requestType = Utils.HTTPMethod.PATCH
    scope = Scope.Channel.Manage.Polls
    authorization = Utils.AuthRequired.USER
    endPoint ="/polls"

    def __init__(self, broadcaster_id: str, id: str, status: str) -> None:
        self.broadcaster_id = broadcaster_id
        self.id = id
        self.status = status
        super().__init__()


class EndPollResponse(Utils.ResponseBaseClass):
    def __init__(self) -> None:
        super().__init__(None)