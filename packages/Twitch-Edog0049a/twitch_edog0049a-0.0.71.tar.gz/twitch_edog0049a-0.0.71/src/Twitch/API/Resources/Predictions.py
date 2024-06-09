from Twitch.API.Resources.__imports import *

class GetPredictionsRequest(Utils.RequestBaseClass):
    requestType = Utils.HTTPMethod.GET
    scope = [Scope.Channel.Read.Predictions, Scope.Channel.Manage.Predictions]
    authorization = Utils.AuthRequired.USER
    endPoint ="/predictions"
    def __init__(self, broadcaster_id: str, id:str=Optional[str], first: Optional[str]=None, after:Optional[str]=None) -> None:
        self.broadcaster_id = broadcaster_id
        self.id = id
        self.first = first
        self.after = after
        super().__init__()

ACTIVE = "ACTIVE"
RESOLVED = "RESOLVED"
CANCELED = "CANCELED"
LOCKED = "LOCKED"
Status = TypeVar("Status", "ACTIVE", "RESOLVED", "CANCELED", "LOCKED") 
     
class Predictor:
    user_id: str
    user_login: str
    user_name: str
    channel_points_won: int
    channel_points_used: int

class Outcome:
    id: str
    title: str
    users: int
    channel_points: int
    top_predictors: List[Predictor]
    color: str

class Prediction:
    id: str
    broadcaster_id: str
    broadcaster_name: str
    broadcaster_login: str
    title: str
    winning_outcome_id: str
    outcomes: List[Outcome]
    prediction_window: int
    status: str
    created_at: str
    ended_at: str
    locked_at: str
    

class GetPredictionsResponse(Utils.PagenationMixin, Utils.ResponseBaseClass):
        def __init__(self) -> None:
            super().__init__(Prediction)

class OutcomeItem:
    title: str

class CreatePredictionRequest(Utils.RequestBaseClass):
    requestType = Utils.HTTPMethod.POST
    scope = Scope.Channel.Manage.Predictions
    authorization = Utils.AuthRequired.USER
    endPoint ="/predictions"
    def __init__(self, broadcaster_id: str, title: str, outcomes: List[OutcomeItem], prediction_window: int) -> None:
        self.broadcaster_id = broadcaster_id
        self.title = title
        self.outcomes = outcomes
        self.prediction_window = prediction_window
        super().__init__()

class CreatePredictionResponse(Utils.ResponseBaseClass):
        def __init__(self) -> None:
            super().__init__(Prediction)

class EndPredictionRequest(Utils.RequestBaseClass):
    requestType = Utils.HTTPMethod.PATCH
    scope = Scope.Channel.Manage.Predictions
    authorization = Utils.AuthRequired.USER
    endPoint ="/predictions"
    def __init__(self, broadcaster_id: str, id: str, status: Status) -> None:
        self.broadcaster_id = broadcaster_id
        self.id = id
        self.status = status
        super().__init__()
    

class EndPredictionResponse(Utils.ResponseBaseClass):
        def __init__(self) -> None:
            super().__init__(Prediction)