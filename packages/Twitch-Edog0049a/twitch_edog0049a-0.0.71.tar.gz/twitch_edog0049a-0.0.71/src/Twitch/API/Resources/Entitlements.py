from Twitch.API.Resources.__imports import *

class GetDropsEntitlementsRequest(Utils.RequestBaseClass):
    requestType = Utils.HTTPMethod.GET
    scope = None
    authorization = Utils.AuthRequired.CLIENT
    endPoint ="/entitlements/drops"

    def __init__(self,id: Optional[str]=None, user_id: Optional[str]=None, 
                game_id: Optional[str]=None, fulfillment_status:Optional[str]=None,
                after:Optional[str]=None, first:Optional[int]=None, userAuth: bool=False) -> None:
        if userAuth:
            self.authorization = Utils.AuthRequired.USER
        self.id = id
        self.user_id = user_id
        self.game_id = game_id
        self.fulfillment_status = fulfillment_status
        self.after = after
        self.first = first
        super().__init__()
      
class GetDropsEntitlementsItem:
    id: str
    benefit_id: str 
    timestamp: str
    user_id: str
    game_id: str
    fulfillment_status: str 
    entitlement_id: str
    last_updated: str

class GetDropsEntitlementsResponse(Utils.pagenation, Utils.ResponseBaseClass):
    def __init__(self) -> None:
        super().__init__(GetDropsEntitlementsItem)

class UpdateDropsEntitlementsRequest(Utils.RequestBaseClass):
    requestType = Utils.HTTPMethod.PATCH
    scope = None
    authorization = Utils.AuthRequired.CLIENT
    endPoint ="/entitlements/drops"

    def __init__(self, entitlement_ids: Optional[list[str]]=None, fulfillment_status:Optional[str]=None, userAuth: bool=False) -> None:
        if userAuth:
            self.authorization = Utils.AuthRequired.USER
        self.entitlement_ids = entitlement_ids
        self.fulfillment_status = fulfillment_status
        super().__init__()

class UpdateDropsEntitlementsItem:
     status: str
     ids: list[str]

class UpdateDropsEntitlementsResponse(Utils.ResponseBaseClass):
    def __init__(self) -> None:
        super().__init__(UpdateDropsEntitlementsItem)