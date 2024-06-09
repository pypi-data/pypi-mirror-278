from Twitch.API.Resources.__imports import *

class Transport:
    callback: str
    method: str
    secret: str
    session_id: str
    connected_at: str
    disconnected_at	: str

class CreateEventSubSubscriptionRequest(Utils.RequestBaseClass):
    requestType = Utils.HTTPMethod.POST
    scope = Scope.Channel.Read.Subscriptions
    authorization = Utils.AuthRequired.CLIENT
    endPoint ="/eventsub/subscriptions"
    def __init__(self,type: str, version: str, condition: str, transport: Transport ) -> None:
        self.type = type
        self.version = version
        self.condition = condition
        self.transport = transport        
        super().__init__()
    
class CreateEventSubSubscriptionItem:
    id: str
    status: str
    type: str
    version: str
    condition: str
    created_at: str
    transport: Transport
    cost: int

class CreateEventSubSubscriptionResponse(Utils.ResponseBaseClass):
    total: int
    total_cost: int
    max_total_cost: int
    def __init__(self) -> None:
        super().__init__(CreateEventSubSubscriptionItem)

class DeleteEventSubSubscriptionRequest(Utils.RequestBaseClass):
    requestType = Utils.HTTPMethod.DELETE
    scope = Scope.Channel.Read.Subscriptions
    authorization = Utils.AuthRequired.CLIENT
    endPoint ="/eventsub/subscriptions"
    def __init__(self, id: str) -> None:
        self.id = id
        super().__init__()


class DeleteEventSubSubscriptionResponse(Utils.ResponseBaseClass):
        def __init__(self) -> None:
            super().__init__(None)

class GetEventSubSubscriptionsRequest(Utils.RequestBaseClass):
    requestType = Utils.HTTPMethod.GET
    scope = None
    authorization = Utils.AuthRequired.CLIENT
    endPoint ="/eventsub/subscriptions"
    def __init__(self, status: Optional[str]=None, type: Optional[str]=None,user_id: Optional[str]=None, after: Optional[str]=None) -> None:
        self.status = status
        self.type = type
        self.after = after
        self.user_id = user_id
        super().__init__()
    
class GetEventSubSubscriptionsItem:
    id: str
    status: str
    type: str
    version: str
    condition: str
    created_at: str
    transport: Transport
    cost: int

class GetEventSubSubscriptionsResponse(Utils.PagenationMixin, Utils.ResponseBaseClass):
    total: int 
    total_cost: int
    max_total_cost: int

    def __init__(self) -> None:
        super().__init__(GetEventSubSubscriptionsItem)