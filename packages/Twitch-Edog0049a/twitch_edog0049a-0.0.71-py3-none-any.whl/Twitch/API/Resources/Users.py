from Twitch.API.Resources.__imports import *

class GetUsersRequest(Utils.RequestBaseClass):
    requestType = Utils.HTTPMethod.GET
    scope = Scope.User.Read.Email
    authorization = Utils.AuthRequired.CLIENT
    endPoint ="/users"
    def __init__(self, id: Optional[str|list] = None, login: Optional[str|list]=None, userAuth=False) -> None:
        if userAuth:
            self.authorization = Utils.AuthRequired.USER
        self.id =   id  
        self.login = login
        super().__init__()

class User:
    id: str 
    login: str 
    display_name: str 
    type: str
    broadcaster_type: str 
    description: str
    profile_image_url: str
    offline_image_url: str 
    view_count: int
    email: str
    created_at: str

class GetUsersResponse(Utils.ResponseBaseClass):
    def __init__(self) -> None:
        super().__init__(User)

class UpdateUserRequest(Utils.RequestBaseClass):
    requestType = Utils.HTTPMethod.PUT
    scope = Scope.User.Edit
    authorization = Utils.AuthRequired.USER
    endPoint ="/users"
    def __init__(self, description: str) -> None:
        self.description = description
        super().__init__()


class UpdateUserResponse(Utils.ResponseBaseClass):
    def __init__(self) -> None:
        super().__init__(User)


class GetUserBlockListRequest(Utils.RequestBaseClass):
    requestType = Utils.HTTPMethod.GET
    scope = Scope.User.Read.Blocked_users
    authorization = Utils.AuthRequired.USER
    endPoint ="/users/blocks"
    def __init__(self, broadcaster_id: str, first: Optional[int]=None, After: Optional[str]=None) -> None:
        self.broadcaster_id = broadcaster_id
        self.first = first
        self.After = After
        super().__init__()
class BlockedUser:
    user_id: str
    user_login: str
    display_name: str

class GetUserBlockListResponse(Utils.ResponseBaseClass):
    def __init__(self) -> None:
        super().__init__(BlockedUser)

class BlockUserRequest(Utils.RequestBaseClass):
    requestType = Utils.HTTPMethod.PUT
    scope = Scope.User.Manage.Blocked_users
    authorization = Utils.AuthRequired.USER
    endPoint ="/users/blocks"
    def __init__(self, target_user_id: str, source_context: Optional[str]=None, reason: Optional[str]=None) -> None:
        self.target_user_id = target_user_id
        self.source_context = source_context
        self.reason = reason
        super().__init__()
    

class BlockUserResponse(Utils.ResponseBaseClass):
    def __init__(self) -> None:
        super().__init__(None)

class UnblockUserRequest(Utils.RequestBaseClass):
    requestType = Utils.HTTPMethod.DELETE
    scope = Scope.User.Manage.Blocked_users
    authorization = Utils.AuthRequired.USER
    endPoint ="/users/blocks"
    def __init__(self, target_user_id: str) -> None:
        self.target_user_id = target_user_id
        super().__init__()


class UnblockUserResponse(Utils.ResponseBaseClass):
    def __init__(self) -> None:
        super().__init__(None)

class GetUserExtensionsRequest(Utils.RequestBaseClass):
    requestType = Utils.HTTPMethod.GET
    scope = [Scope.User.Read.Broadcast, Scope.User.Edit]
    authorization = Utils.AuthRequired.USER
    endPoint ="/users/extensions/list"
    def __init__(self) -> None:
        super().__init__()

class Extension:
    id: str
    version: str
    name: str
    can_activate: bool
    type: str


class GetUserExtensionsResponse(Utils.ResponseBaseClass):
    def __init__(self) -> None:
        super().__init__(Extension)

class GetUserActiveExtensionsRequest(Utils.RequestBaseClass):
    requestType = Utils.HTTPMethod.GET
    scope = None
    authorization = Utils.AuthRequired.CLIENT
    endPoint ="/users/extensions"
    def __init__(self, user_id: Optional[str]=None, userAuth=False) -> None:
        self.user_id = user_id
        if userAuth or user_id==None:
            self.authorization = Utils.AuthRequired.USER
        super().__init__()
 
class ExtensionItem:
    active: bool
    id: str
    version: str
    name: str
    x: int
    y: int

class ActiveExtension:
    panel: dict[str, ExtensionItem]
    overlay: dict[str, ExtensionItem]
    component: dict[str, ExtensionItem]

class GetUserActiveExtensionsResponse(Utils.ResponseBaseClass):
    def __init__(self) -> None:
        super().__init__(ActiveExtension)

class UpdateUserExtensionsRequest(Utils.RequestBaseClass):
    requestType = Utils.HTTPMethod.POST
    scope = Scope.User.Edit
    authorization = Utils.AuthRequired.USER
    endPoint ="/users/extensions"
    def __init__(self, panel: Optional[dict[str, ExtensionItem]]=None, overlay: Optional[dict[str, ExtensionItem]]=None, component: Optional[dict[str, ExtensionItem]]=None) -> None:
        self.data: dict[str, dict[str, ExtensionItem]] = {}
        if panel:
            self.data["panel"] = panel
        if overlay:
            self.data["overlay"] = overlay
        if component:
            self.data["component"] = component
        super().__init__()
    

class UpdateUserExtensionsResponse(Utils.ResponseBaseClass):
    def __init__(self) -> None:
        super().__init__(ActiveExtension)

