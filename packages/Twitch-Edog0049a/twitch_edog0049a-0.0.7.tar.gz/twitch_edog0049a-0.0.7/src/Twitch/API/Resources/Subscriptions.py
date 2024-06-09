from Twitch.API.Resources.__imports import *

class GetBroadcasterSubscriptionsRequest(Utils.RequestBaseClass):
        requestType = Utils.HTTPMethod.GET
        scope = Scope.Channel.Read.Subscriptions
        authorization = Utils.AuthRequired.USER
        endPoint ="/subscriptions"
        def __init__(self, broadcaster_id: str, user_id: Optional[str]=None, after: Optional[str]=None, before: Optional[str]=None, first: Optional[int]=None) -> None:
                self.broadcaster_id = broadcaster_id
                self.user_id = user_id
                self.after = after
                self.before = before
                self.first = first
                super().__init__()

class Subscription:
        broadcaster_id: str
        broadcaster_login: str
        broadcaster_name: str
        gifter_id: str
        gifter_login: str
        gifter_name: str
        is_gift: bool
        tier: str
        plan_name: str
        user_id: str
        user_login: str
        user_name: str
    
class GetBroadcasterSubscriptionsResponse(Utils.PagenationMixin, Utils.ResponseBaseClass):
        total: int
        points: int
        def __init__(self) -> None:
            super().__init__(Subscription)

class CheckUserSubscriptionRequest(Utils.RequestBaseClass):
        requestType = Utils.HTTPMethod.POST
        scope = Scope.User.Read.Subscriptions
        authorization = Utils.AuthRequired.USER
        endPoint ="/subscriptions/user"
        def __init__(self, broadcaster_id: str, user_id: str) -> None:
                self.broadcaster_id = broadcaster_id
                self.user_id = user_id
                super().__init__()
    
class CheckUserSubscriptionResponse(Utils.ResponseBaseClass):
        def __init__(self) -> None:
            super().__init__(Subscription)
