from Twitch.API.Resources.__imports import *

#msg_id = TypeAlias(str, "Message ID")
#msg_text = TypeAlias(str, "Message Text")

class CheckAutoModStatusRequest(Utils.RequestBaseClass):
    requestType = Utils.HTTPMethod.POST
    scope = Scope.Moderation.Read
    authorization = Utils.AuthRequired.USER
    endPoint ="/moderation/enforcements/status"
    def __init__(self, broadcaster_id: str, data: List[Tuple]) -> None:
        """
        __init__ Takes in the required parameters for CheckAutoModStatusRequest, and auto generates the request body.

        usage: CheckAutoModStatusRequest(broadcaster_id, [(msg_id, msg_text), (msg_id, msg_text), ...])

        :param broadcaster_id: The broadcaster ID associated with the request.
        :type broadcaster_id: str
        :param data: date takes in a list of tuples, each tuple is a Message id and a Message.
        :type data: List[tuple[str, str]]
        """
        self.broadcaster_id = broadcaster_id
        self.data = data
        super().__init__()

class MsgStatus:
       msg_id: str
       is_permitted: bool

class CheckAutoModStatusResponse(Utils.ResponseBaseClass):
    """    
    CheckAutoModStatusResponse is a list of MsgStatus objects.

    MsgStatus is a class with two attributes, msg_id and is_permitted.
    """
    def __init__(self) -> None:
        super().__init__(MsgStatus)

class ManageHeldAutoModMessagesRequest(Utils.RequestBaseClass):
    requestType = Utils.HTTPMethod.POST
    scope = Scope.Moderator.Manage.Automod
    authorization = Utils.AuthRequired.USER
    endPoint ="/moderation/automod/message"
    DENY = "DENY"
    APPROVE = "APPROVE"
    Action = TypeVar("Action", "DENY", "APPROVE")
    def __init__(self, user_id: str, msg_id: str, action: Action ) -> None:
        """
        __init__ applies an action to a held message.

        usage: ManageHeldAutoModMessagesRequest(user_id, msg_id, action)

        :param user_id: user id of the user who sent the message.
        :type user_id: str
        :param msg_id: id of the message to take action on.
        :type msg_id: str
        :param action: The action to take on the message. Valid values are DENY and APPROVE.
        :type action: Action
        """
        self.user_id = user_id
        self.msg_id = msg_id
        self.action = action
        super().__init__()

class ManageHeldAutoModMessagesResponse(Utils.ResponseBaseClass):
    def __init__(self) -> None:
        """
        ManageHeldAutoModMessagesResponse is a response object with no data.
        check the status attribute to see if the request was successful.
        """
        super().__init__(None)

class GetAutoModSettingsRequest(Utils.RequestBaseClass):
        requestType = Utils.HTTPMethod.GET  
        scope = Scope.Moderator.Read.Automod_settings
        authorization = Utils.AuthRequired.USER
        endPoint ="/moderation/automod/settings"
        def __init__(self, broadcaster_id: str, moderator_id: str) -> None:
            """
            __init__  gets the AutoMod settings for a channel.

            usage: GetAutoModSettingsRequest(broadcaster_id, moderator_id)

            :param broadcaster_id: broadcaster ID associated with the request.
            :type broadcaster_id: str
            :param moderator_id: user ID of the broadcaster or moderator requesting the settings, must match user access token.
            :type moderator_id: str
            """
            self.broadcaster_id = broadcaster_id
            self.moderator_id = moderator_id
            super().__init__()

class AutoModSettings:
    broadcaster_id: str
    moderator_id: str
    overall_level: int
    disability: int
    aggression: int
    sexuality_sex_or_gender: int
    misognyny: int
    bullying: int
    swearing: int
    race_ethnicity_or_religion: int
    sex_based_terms: int
    
class GetAutoModSettingsResponse(Utils.ResponseBaseClass):
        def __init__(self) -> None:
            super().__init__(AutoModSettings)

class UpdateAutoModSettingsRequest(Utils.RequestBaseClass):
    requestType = Utils.HTTPMethod.PUT
    scope = Scope.Moderator.Manage.Automod_settings
    authorization = Utils.AuthRequired.USER
    endPoint ="/moderation/automod/settings"
    def __init__(self, broadcaster_id: str, moderator_id: str, data: List[AutoModSettings]) -> None:
        """
        __init__ updates the AutoMod settings for a channel.

        usage: UpdateAutoModSettingsRequest(broadcaster_id, moderator_id, data)

        :param broadcaster_id: broadcaster ID associated with the request.
        :type broadcaster_id: str
        :param moderator_id: user ID of the broadcaster or moderator requesting the settings, must match user access token.
        :type moderator_id: str
        :param data: data is a list of AutoModSettings objects.
        :type data: List[AutoModSettings]
        """
        self.broadcaster_id = broadcaster_id
        self.moderator_id = moderator_id
        self.data = data
        super().__init__()
        
class UpdateAutoModSettingsResponse(Utils.ResponseBaseClass):
    def __init__(self) -> None:
        super().__init__(AutoModSettings)

class GetBannedUsersRequest(Utils.RequestBaseClass):
    requestType = Utils.HTTPMethod.GET
    scope = [Scope.Moderation.Read, Scope.Moderator.Manage.Banned_users]
    authorization = Utils.AuthRequired.USER
    endPoint ="/moderation/banned"
    def __init__(self, broadcaster_id: str, user_id: Optional[List[str]]=None, after: Optional[str]=None, before: Optional[str]=None, first: Optional[int]=None) -> None:
        """
        __init__ gets a list of banned users for a broadcaster.

        usage: GetBannedUsersRequest(broadcaster_id, user_id, after, before, first)

        :param broadcaster_id: broadcaster ID to get banned users.
        :type broadcaster_id: str
        :param user_id:  user ids to filter results.
        :type user_id: List[str]
        :param after: takes pagination cursor to fetch the next set of results.
        :type after: str
        :param before: takes pagination cursor to fetch the previous set of results.
        :type before: str
        :param first:  maximum number of objects to return. Maximum: 100. Default: 20.
        :type first: int
        """
        self.broadcaster_id = broadcaster_id
        self.user_id = user_id
        self.after = after
        self.before = before
        self.first = first

        super().__init__()

class BannedUser:
    user_id: str
    user_name: str
    expires_at: str
    created_at: str
    reason: str
    moderator_id: str
    moderator_login: str
    moderator_name: str

class GetBannedUsersResponse(Utils.ResponseBaseClass):
        def __init__(self) -> None:            
            super().__init__(BannedUser)

class UserBan:
    user_id: str
    duration: int
    reason: str

class BanUserRequest(Utils.RequestBaseClass):
        requestType = Utils.HTTPMethod.POST
        scope = Scope.Moderator.Manage.Banned_users
        authorization = Utils.AuthRequired.USER
        endPoint ="/moderation/bans"
        def __init__(self, broadcaster_id: str, moderator_id: str, data: List[UserBan]) -> None:
            """
            __init__ bans userfrom a channel.

            usage: BanUserRequest(broadcaster_id, moderator_id, data)

            :param broadcaster_id: broadcaster ID associated with the request.
            :type broadcaster_id: str
            :param moderator_id: user ID of the broadcaster or moderator requesting the settings, must match user access token.
            :type moderator_id: str
            :param data: data is a list of UserBan objects.
            :type data: List[UserBan]
            """
            self.broadcaster_id = broadcaster_id
            self.moderator_id = moderator_id
            self.data = data
            super().__init__()

class Ban:
    broadcaster_id: str
    moderator_id: str
    user_id: str
    created_at: str
    end_time: str

class BanUserResponse(Utils.ResponseBaseClass):
        def __init__(self) -> None:
            super().__init__(Ban)

class UnbanUserRequest(Utils.RequestBaseClass):
    requestType = Utils.HTTPMethod.DELETE
    scope = Scope.Moderator.Manage.Banned_users
    authorization = Utils.AuthRequired.USER
    endPoint ="/moderation/bans"
    def __init__(self, broadcaster_id: str, user_id: str, moderator_id: str) -> None:
        """
        __init__ unbans userfrom a channel.

        usage: UnbanUserRequest(broadcaster_id, user_id, moderator_id)

        :param broadcaster_id: broadcaster ID associated with the request.
        :type broadcaster_id: str
        :param user_id: user ID of the user to unban.
        :type user_id: str
        :param moderator_id: user ID of the broadcaster or moderator requesting the settings, must match user access token.
        :type moderator_id: str
        """
        self.broadcaster_id = broadcaster_id
        self.user_id = user_id
        self.moderator_id = moderator_id
        super().__init__()
    

class UnbanUserResponse(Utils.ResponseBaseClass):
    def __init__(self) -> None:
        super().__init__(None)

class GetBlockedTermsRequest(Utils.RequestBaseClass):
    requestType = Utils.HTTPMethod.GET
    scope = [Scope.Moderator.Read.Blocked_terms, Scope.Moderator.Manage.Blocked_terms]
    authorization = Utils.AuthRequired.USER
    endPoint ="/moderation/blocked-terms"
    def __init__(self, broadcaster_id: str, moderator_id: str, first: Optional[int]=None, after: Optional[str]=None) -> None:
        """
        __init__ gets a list of blocked terms for a broadcaster.

        usage: GetBlockedTermsRequest(broadcaster_id, moderator_id, first, after)

        :param broadcaster_id: broadcaster ID associated with the request.
        :type broadcaster_id: str
        :param moderator_id: user ID of the broadcaster or moderator requesting the settings, must match user access token.
        :type moderator_id: str
        :param first: maximum number of objects to return. Maximum: 100. Default: 20.
        :type first: Optional[int]
        :param after: cursor for forward pagination: tells the server where to start fetching the next set of results, in a multi-page response.
        :type after: Optional[str]
        """
        self.broadcaster_id = broadcaster_id
        self.moderator_id = moderator_id
        self.first = first
        self.after = after
        super().__init__()

class BlockedTerm:
    broadcaster_id: str
    moderator_id: str
    id: str
    text: str
    created_at: str
    updated_at: str
    expires_at: str

class GetBlockedTermsResponse(Utils.PagenationMixin, Utils.ResponseBaseClass):
    def __init__(self) -> None:
        super().__init__(BlockedTerm)

class AddBlockedTermRequest(Utils.RequestBaseClass):
    requestType = Utils.HTTPMethod.POST
    scope = Scope.Moderator.Manage.Blocked_terms
    authorization = Utils.AuthRequired.USER
    endPoint ="/moderation/blocked-terms"
    def __init__(self, broadcaster_id: str, moderator_id: str, text:str) -> None:
        """
        __init__ adds a term to a channel’s blocked terms list.

        usage: AddBlockedTermRequest(broadcaster_id, moderator_id, text)

        :param broadcaster_id: broadcaster ID associated with the request.
        :type broadcaster_id: str
        :param moderator_id: user ID of the broadcaster or moderator requesting the settings, must match user access token.
        :type moderator_id: str
        :param text: term to be blocked.
        :type text: str
        """
        self.broadcaster_id = broadcaster_id
        self.moderator_id = moderator_id
        self.text = text
        super().__init__()  

class AddBlockedTermResponse(Utils.ResponseBaseClass):
        def __init__(self) -> None:
            super().__init__(BlockedTerm)

class RemoveBlockedTermRequest(Utils.RequestBaseClass):
    requestType = Utils.HTTPMethod.DELETE
    scope = Scope.Moderator.Manage.Blocked_terms
    authorization = Utils.AuthRequired.USER
    endPoint ="/moderation/blocked-terms"
    def __init__(self, broadcaster_id: str, moderator_id: str, id:str) -> None:
        """
        __init__ deletes a term from a channel’s blocked terms list.

        usage: RemoveBlockedTermRequest(broadcaster_id, moderator_id, id)

        :param broadcaster_id: broadcaster ID associated with the request.
        :type broadcaster_id: str
        :param moderator_id: user ID of the broadcaster or moderator requesting the settings, must match user access token.
        :type moderator_id: str
        :param id: ID of the term to be deleted.
        :type id: str
        """
        self.broadcaster_id = broadcaster_id
        self.moderator_id = moderator_id
        self.id = id
        super().__init__()
    

class RemoveBlockedTermResponse(Utils.ResponseBaseClass):
        def __init__(self) -> None:
            super().__init__(None)

class DeleteChatMessagesRequest(Utils.RequestBaseClass):
        requestType = Utils.HTTPMethod.DELETE
        scope = Scope.Moderator.Manage.Chat_messages
        authorization = Utils.AuthRequired.USER
        endPoint ="/moderation/chat"
        def __init__(self, broadcaster_id: str, moderator_id: str, message_id: Optional[str]=None) -> None:
            """
            __init__ deletes one or more messages from a channel.

            usage: DeleteChatMessagesRequest(broadcaster_id, moderator_id, message_id)

            :param broadcaster_id: broadcaster ID associated with the request.
            :type broadcaster_id: str
            :param moderator_id: user ID of the broadcaster or moderator requesting the settings, must match user access token.
            :type moderator_id: str
            :param message_id: ID of the message to be deleted.
            :type message_id: str
            """
            self.broadcaster_id = broadcaster_id
            self.moderator_id = moderator_id
            self.message_id = message_id
            super().__init__()
    

class DeleteChatMessagesResponse(Utils.ResponseBaseClass):
        def __init__(self) -> None:
            super().__init__(None)

class GetModeratorsRequest(Utils.RequestBaseClass):
    requestType = Utils.HTTPMethod.POST
    scope = [Scope.Channel.Manage.Moderators, Scope.Moderation.Read]
    authorization = Utils.AuthRequired.USER
    endPoint ="/moderation/moderators"
    def __init__(self, broadcaster_id: str, user_id: Optional[str]=None, first: Optional[int]=None, after: Optional[str]=None) -> None:
        """
        __init__ Gets all users allowed to moderate the broadcasters chat roomt.

        usage: GetModeratorsRequest(broadcaster_id, user_id, first, after)

        :param broadcaster_id: broadcaster ID associated with the request.
        :type broadcaster_id: str
        :param user_id: user ID of the broadcaster or moderator requesting the settings, must match user access token.
        :type user_id: str
        :param first: maximum number of objects to return. Maximum: 100. Default: 20.
        :type first: Optional[int]
        :param after: cursor for forward pagination: tells the server where to start fetching the next set of results, in a multi-page response.
        :type after: Optional[str]
        """
        self.broadcaster_id = broadcaster_id
        self.user_id = user_id
        self.first = first
        self.after = after
        super().__init__()

class Modorator:
    user_id: str
    user_login: str
    user_name: str

class GetModeratorsResponse(Utils.PagenationMixin, Utils.ResponseBaseClass):
    def __init__(self) -> None:
        super().__init__(Modorator)

class AddChannelModeratorRequest(Utils.RequestBaseClass):
    requestType = Utils.HTTPMethod.POST
    scope = Scope.Channel.Manage.Moderators
    authorization = Utils.AuthRequired.USER
    endPoint ="/moderation/moderators"
    def __init__(self, broadcaster_id: str, user_id: str) -> None:
        """
        __init__ Adds a specified user to the moderators list of a specified channel.

        usage: AddChannelModeratorRequest(broadcaster_id, user_id)

        :param broadcaster_id: broadcaster ID associated with the request.
        :type broadcaster_id: str
        :param user_id: user ID of the broadcaster or moderator requesting the settings, must match user access token.
        :type user_id: str
        """
        self.broadcaster_id = broadcaster_id
        self.user_id = user_id
        super().__init__()

    

class AddChannelModeratorResponse(Utils.ResponseBaseClass):
    def __init__(self) -> None:
        super().__init__(None)


class RemoveChannelModeratorRequest(Utils.RequestBaseClass):
    requestType = Utils.HTTPMethod.DELETE
    scope = Scope.Channel.Manage.Moderators
    authorization = Utils.AuthRequired.USER
    endPoint ="/moderation/moderators"
    def __init__(self, broadcaster_id: str, user_id: str) -> None:
        """
        __init__ Deletes a specified user from the moderators list of a specified channel.

        usage: RemoveChannelModeratorRequest(broadcaster_id, user_id)

        :param broadcaster_id: broadcaster ID associated with the request.
        :type broadcaster_id: str
        :param user_id: user ID of the broadcaster or moderator requesting the settings, must match user access token.
        :type user_id: str
        """
        self.broadcaster_id = broadcaster_id
        self.user_id = user_id
        super().__init__()
    

class RemoveChannelModeratorResponse(Utils.ResponseBaseClass):
    def __init__(self) -> None:
        super().__init__(None)

class GetVIPsRequest(Utils.RequestBaseClass):
    requestType = Utils.HTTPMethod.GET
    scope = [Scope.Channel.Read.Vips, Scope.Channel.Manage.Vips]
    authorization = Utils.AuthRequired.USER
    endPoint ="/channels/vips"
    def __init__(self, broadcaster_id: str, user_id: Optional[str]=None, first: Optional[int]=None, after: Optional[str]=None) -> None:
        """
        __init__ Gets all users in a channel's VIP list.

        usage: GetVIPsRequest(broadcaster_id, user_id, first, after)

        :param broadcaster_id: broadcaster ID associated with the request.
        :type broadcaster_id: str
        :param user_id: user ID of the broadcaster or moderator requesting the settings, must match user access token.
        :type user_id: str
        :param first: maximum number of objects to return. Maximum: 100. Default: 20.
        :type first: Optional[int]
        :param after: cursor for forward pagination: tells the server where to start fetching the next set of results, in a multi-page response.
        :type after: Optional[str]
        """
        self.broadcaster_id = broadcaster_id
        self.user_id = user_id
        self.first = first
        self.after = after
        super().__init__()

class Vip:
    user_id: str
    user_login: str
    user_name: str

class GetVIPsResponse(Utils.PagenationMixin, Utils.ResponseBaseClass):
    def __init__(self) -> None:
        super().__init__(Vip)

class AddChannelVIPRequest(Utils.RequestBaseClass):
    requestType = Utils.HTTPMethod.POST
    scope = Scope.Channel.Manage.Vips
    authorization = Utils.AuthRequired.USER
    endPoint ="/channels/vips"
    def __init__(self, broadcaster_id: str, user_id: str) -> None:
        """
        __init__ Adds a specified user to the VIP list of a specified channel.

        usage: AddChannelVIPRequest(broadcaster_id, user_id)

        :param broadcaster_id: broadcaster ID associated with the request.
        :type broadcaster_id: str
        :param user_id: user ID of the broadcaster or moderator requesting the settings, must match user access token.
        :type user_id: str
        """
        self.broadcaster_id = broadcaster_id
        self.user_id = user_id
        super().__init__()

class AddChannelVIPResponse(Utils.ResponseBaseClass):
    def __init__(self) -> None:
        super().__init__(None)

class RemoveChannelVIPRequest(Utils.RequestBaseClass):
    requestType = Utils.HTTPMethod.DELETE
    scope = Scope.Channel.Manage.Vips
    authorization = Utils.AuthRequired.USER
    endPoint ="/channels/vips"
    def __init__(self, broadcaster_id: str, user_id: str) -> None:
        """
        __init__ Deletes a specified user from the VIP list of a specified channel.

        usage: RemoveChannelVIPRequest(broadcaster_id, user_id)

        :param broadcaster_id: broadcaster ID associated with the request.
        :type broadcaster_id: str
        :param user_id: user ID of the broadcaster or moderator requesting the settings, must match user access token.
        :type user_id: str
        """
        self.broadcaster_id = broadcaster_id
        self.user_id = user_id
        super().__init__()

class RemoveChannelVIPResponse(Utils.ResponseBaseClass):
        def __init__(self) -> None:
            super().__init__(None)

class UpdateShieldModeStatusRequest(Utils.RequestBaseClass):
    requestType = Utils.HTTPMethod.PUT
    scope = Scope.Moderator.Manage.Shield_mode
    authorization = Utils.AuthRequired.USER
    endPoint ="/moderation/shield_mode"
    def __init__(self, broadcaster_id: str, moderator_id: str, is_active: bool) -> None:
        """
        __init__ Activates or deactivates the broadcasters Shield Mode..

        usage: UpdateShieldModeStatusRequest(broadcaster_id, moderator_id, is_active)

        Twitch's Shield Mode feature is like a panic button that broadcasters can push to protect themselves from chat abuse coming from one or more accounts. 
        When activated, Shield Mode applies the overrides that the broadcaster configured in the Twitch UX. 
        If the broadcaster hasn't configured Shield Mode, it applies default overrides.

        :param broadcaster_id: broadcaster ID associated with the request.
        :type broadcaster_id: str
        :param moderator_id: user ID of the broadcaster or moderator requesting the settings, must match user access token.
        :type moderator_id: str
        :param is_active: If true, enables Shield Mode. If false, disables Shield Mode.
        :type is_active: bool
        """
        self.broadcaster_id = broadcaster_id
        self.moderator_id = moderator_id
        self.is_active = is_active
        super().__init__() 

class ShieldMode:
    is_active: bool
    moderator_id: str
    moderator_login: str   
    moderator_name: str
    last_activated_at: str

class UpdateShieldModeStatusResponse(Utils.ResponseBaseClass):
        def __init__(self) -> None:
            super().__init__(ShieldMode)

class GetShieldModeStatusRequest(Utils.RequestBaseClass):
    requestType = Utils.HTTPMethod.GET
    scope = [Scope.Moderator.Read.Shield_mode, Scope.Moderator.Manage.Shield_mode]
    authorization = Utils.AuthRequired.USER
    endPoint ="/moderation/shield_mode"
    def __init__(self, broadcaster_id: str, moderator_id: str) -> None:
        """
        __init__ Gets the status of the broadcaster's Shield Mode.

        usage: GetShieldModeStatusRequest(broadcaster_id, moderator_id)

        :param broadcaster_id: broadcaster ID associated with the request.
        :type broadcaster_id: str
        :param moderator_id: user ID of the broadcaster or moderator requesting the settings, must match user access token.
        :type moderator_id: str
        """
        self.broadcaster_id = broadcaster_id
        self.moderator_id = moderator_id
        super().__init__()

class GetShieldModeStatusResponse(Utils.ResponseBaseClass):
        def __init__(self) -> None:
            super().__init__(ShieldMode)
