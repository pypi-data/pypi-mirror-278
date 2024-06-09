from Twitch.API.Resources.__imports import *

class GetExtensionConfigurationSegmentRequest(Utils.RequestBaseClass):
    requestType = Utils.HTTPMethod.GET
    scope = None
    authorization = Utils.AuthRequired.JTW
    endPoint ="/extensions/configurations"
    def __init__(self,extension_id: str, segment: str, broadcaster_id: Optional[str]=None) -> None:
        self.extension_id = extension_id        
        self.segment = segment
        self.broadcaster_id = broadcaster_id
        super().__init__()

class GetExtensionConfigurationSegmentItem:
    broadcaster_id: str
    segment: str
    version: str
    content: str 

class GetExtensionConfigurationSegmentResponse(Utils.ResponseBaseClass):
    def __init__(self) -> None:
        super().__init__(GetExtensionConfigurationSegmentItem)

class SetExtensionConfigurationSegmentRequest(Utils.RequestBaseClass):
    requestType = Utils.HTTPMethod.PUT
    scope = None
    authorization = Utils.AuthRequired.JTW
    endPoint ="/extensions/configurations"
    def __init__(self, extension_id: str, segment: str, broadcaster_id: Optional[str]=None, content: Optional[str]=None, version: Optional[str]=None) -> None:
        self.extension_id = extension_id
        self.segment = segment
        self.broadcaster_id = broadcaster_id
        self.content = content
        self.version = version
        super().__init__()
    

class SetExtensionConfigurationSegmentResponse(Utils.ResponseBaseClass):
        def __init__(self) -> None:
            super().__init__(None)

class SetExtensionRequiredConfigurationRequest(Utils.RequestBaseClass):
    requestType = Utils.HTTPMethod.PUT
    scope = None
    authorization = Utils.AuthRequired.JTW
    endPoint ="/extensions/required_configuration"
    def __init__(self, broadcaster_id: str, extension_id: str, extension_version: str, required_configuration: str) -> None:
        """
        __init__ used to set the required parameters for the request before activating extension

        usage: SetExtensionRequiredConfigurationRequest(broadcaster_id, extension_id, extension_version, required_configuration)

        :param broadcaster_id: The ID of the broadcaster that installed the extension on their channel.
        :type broadcaster_id: str
        :param extension_id: The ID of the extension to update.
        :type extension_id: str
        :param extension_version: The ID of the broadcaster that installed the extension on their channel.
        :type extension_version: str
        :param required_configuration:	The required_configuration string to use with the extension.
        :type required_configuration: str
        """
        self.broadcaster_id = broadcaster_id
        self.extension_id = extension_id
        self.extension_version = extension_version
        self.required_configuration = required_configuration
        super().__init__()


class SetExtensionRequiredConfigurationResponse(Utils.ResponseBaseClass):
        def __init__(self) -> None:
            super().__init__(None)

class SendExtensionPubSubMessageRequest(Utils.RequestBaseClass):
    requestType = Utils.HTTPMethod.POST
    scope = None
    authorization = Utils.AuthRequired.JTW
    endPoint ="/extensions/pubsub"
    BROADCAST = "broadcast"
    GLOBAL = "global"
    WHISPER = "whisper-"
    Target = TypeVar("Target", BROADCAST, GLOBAL, WHISPER)
    def __init__(self, target: Target, broadcatser_id: str, is_global_broadcast: bool, message: str) -> None:
        """
        __init__  used to broadcast a message to users of an extension.

        usage: SendExtensionPubSubMessageRequest(target, broadcatser_id, is_global_broadcast, message)

        :param target: The type of target for the message. Valid values are: broadcast, global, and whisper-<user ID>.
        :type target: str
        :param broadcatser_id: The ID of the broadcaster that installed the extension on their channel.
        :type broadcatser_id: str
        :param is_global_broadcast: Whether the message should be broadcast to all viewers of the channel.
        :type is_global_broadcast: bool
        :param message: The message to send.
        :type message: str
        """
        if target == self.WHISPER:
            self.target = target + broadcatser_id
        else:
            self.target = target
        
        self.broadcatser_id = broadcatser_id
        self.is_global_broadcast = is_global_broadcast
        self.message = message
        super().__init__()
    

class SendExtensionPubSubMessageResponse(Utils.ResponseBaseClass):
    def __init__(self) -> None:
        super().__init__(None)

class GetExtensionLiveChannelsRequest(Utils.RequestBaseClass):
    requestType = Utils.HTTPMethod.GET
    scope = None
    authorization = Utils.AuthRequired.CLIENT
    endPoint ="/extensions/live"
    def __init__(self, extension_id: str, after: Optional[str]=None, first: Optional[int]=None, userAuth: bool=False) -> None:
        """
        __init__ used to get the list of channels that have installed the specified extension and have it activated.

        usage: GetExtensionLiveChannelsRequest(extension_id, after, first)

        :param extension_id: The ID of the extension to get the list of channels for.
        :type extension_id: str
        :param after: Cursor for forward pagination: tells the server where to start fetching the next set of results, in a multi-page response.
        :type after: str
        :param first: Maximum number of objects to return. Maximum: 100. Default: 20.
        :type first: int
        """
        if userAuth:
            self.authorization = Utils.AuthRequired.USER
        self.extension_id = extension_id
        self.after = after
        self.first = first
        super().__init__()
    
class ActiveExtension:
    broadcaster_id: str
    broadcaster_name: str
    game_name: str
    game_id: str
    title:str

class GetExtensionLiveChannelsResponse(Utils.PagenationMixin, Utils.ResponseBaseClass):
    def __init__(self) -> None:
        super().__init__(ActiveExtension)

class GetExtensionSecretsRequest(Utils.RequestBaseClass):
    requestType = Utils.HTTPMethod.GET
    scope = None
    authorization = Utils.AuthRequired.JTW
    endPoint ="/extensions/jtw/secrets"
    def __init__(self, extension_id: str) -> None:
        """
        __init__ used to get the secrets for an extension.

        usage: GetExtensionSecretsRequest(extension_id)

        :param extension_id: The ID of the extension to get the secrets for.
        :type extension_id: str
        """
        self.extension_id = extension_id
        super().__init__()
class secret:
    content: str
    active_at: str
    expires_at: str

class ExtensionSecrets:
    format_version: str
    secrets: List[secret]

class GetExtensionSecretsResponse(Utils.ResponseBaseClass):
        def __init__(self) -> None:
            super().__init__(ExtensionSecrets)


class CreateExtensionSecretRequest(Utils.RequestBaseClass):
    requestType = Utils.HTTPMethod.POST
    scope = None
    authorization = Utils.AuthRequired.JTW
    endPoint ="/extensions/jtw/secrets"
    def __init__(self, extension_id: str, delay: Optional[int]=None) -> None:
        """
        __init__ used to create a secret for an extension.

        usage: CreateExtensionSecretRequest(extension_id, delay)

        :param extension_id: The ID of the extension to create the secret for.
        :type extension_id: str
        :param delay: The time, in seconds, before the secret expires. The minimum value is 60 seconds; the maximum value is 86400 seconds (one day). If a value isn’t specified, the default value is 1800 seconds (30 minutes).
        :type delay: int
        """
        self.extension_id = extension_id
        self.delay = delay
        super().__init__()
    

class CreateExtensionSecretResponse(Utils.ResponseBaseClass):
        def __init__(self) -> None:
            super().__init__(ExtensionSecrets)


class SendExtensionChatMessageRequest(Utils.RequestBaseClass):
    requestType = Utils.HTTPMethod.POST
    scope = None
    authorization = Utils.AuthRequired.JTW
    endPoint ="/extensions/chat"
    def __init__(self, broadcaster_id: str, text: str, extension_id: str, extension_version: str) -> None:
        """
        __init__ used to send a chat message to a specified channel.

        usage: SendExtensionChatMessageRequest(broadcaster_id, text, extension_id, extension_version)

        :param broadcaster_id: The ID of the channel to send the message to.
        :type broadcaster_id: str
        :param text: The message text.
        :type text: str
        :param extension_id: The ID of the extension sending the message.
        :type extension_id: str
        :param extension_version: The version of the extension.
        :type extension_version: str
        """
        self.broadcaster_id = broadcaster_id
        self.text = text
        self.extension_id = extension_id
        self.extension_version = extension_version
        super().__init__()

class SendExtensionChatMessageResponse(Utils.ResponseBaseClass):
        def __init__(self) -> None:
            super().__init__(None)

class GetExtensionsRequest(Utils.RequestBaseClass):
    requestType = Utils.HTTPMethod.GET
    scope = None
    authorization = Utils.AuthRequired.CLIENT
    endPoint ="/extensions"
    def __init__(self, extension_id: str, extension_version: Optional[str]=None) -> None:
        """
        __init__ used to get information about extensions installed by a specified user.

        usage: GetExtensionsRequest(extension_id, extension_version)

        :param extension_id: The ID of the extension to get information about.
        :type extension_id: str
        :param extension_version: The version of the extension to get information about. If omitted, returns the active version of the extension.
        :type extension_version: str
        """
        self.extension_id = extension_id
        self.extension_version = extension_version
        super().__init__()
class MobileVeiw:
    viewer_url: str

class PanelView:
    height: int
    viewer_url: str
    can_link_external_content: bool

class VideoOverlayView:
    viewer_url: str
    can_link_external_content: bool
Config: TypeAlias = VideoOverlayView

class Component:
    viewer_url: str
    aspect_ratio_x: int
    aspect_ratio_y: int
    autoscale: bool
    scale_pixels: int
    target_hieght: int
    can_link_external_content: bool
class ExtensionViews:
    mobile: MobileVeiw
    panel: PanelView
    video_overlay: VideoOverlayView
    component: Component
    config: Config
  
class ExtensionComponent:
    author_name: str
    bits_enabled: bool
    can_install: bool
    configuration_location: str
    description: str
    eula_tos_url: str
    has_chat_support: bool
    icon_url: str
    icon_urls: Dict[str, str]
    id: str
    name: str
    privacy_policy_url: str
    request_identity_link: bool
    screenschot_urls: List[str]
    state: str
    subscription_support_level: str
    summary: str
    support_email: str
    version: str
    viewer_summary: str
    views: ExtensionViews
    allowlisted_config_urls: List[str]
    allowlisted_panel_urls: List[str]
   
class GetExtensionsResponse(Utils.ResponseBaseClass):
        def __init__(self) -> None:
            super().__init__(ExtensionComponent)

class GetReleasedExtensionsRequest(Utils.RequestBaseClass):
    requestType = Utils.HTTPMethod.GET
    scope = None
    authorization = Utils.AuthRequired.CLIENT
    endPoint ="/extensions/released"
    def __init__(self, extension_id: str, extension_version: Optional[str]=None, userAuth: bool=False) -> None:
        """
        __init__ used to get information about extensions installed by a specified user.

        usage: GetExtensionsRequest(extension_id, extension_version)

        :param extension_id: The ID of the extension to get information about.
        :type extension_id: str
        :param extension_version: The version of the extension to get information about. If omitted, returns the active version of the extension.
        :type extension_version: str
        """
        if userAuth:
            self.authorization = Utils.AuthRequired.USER
        self.extension_id = extension_id
        self.extension_version = extension_version
        super().__init__()
    

class GetReleasedExtensionsResponse(Utils.ResponseBaseClass):
        def __init__(self) -> None:
            super().__init__(ExtensionComponent)

class GetExtensionBitsProductsRequest(Utils.RequestBaseClass):
        requestType = Utils.HTTPMethod.GET
        scope = None
        authorization = Utils.AuthRequired.CLIENT
        endPoint ="/bits/extensions"
        def __init__(self, should_include_all: Optional[bool]=None):
            """
            __init__ 

            _extended_summary_

            :param should_include_all: _description_, defaults to None
            :type should_include_all: Optional[bool], optional
            """
            self.should_include_all = should_include_all
            super().__init__()
class ExtensionCost:
    type: str
    amount: int

class ExtensionProduct:
    sku: str
    cost: ExtensionCost
    displayName: str
    inDevelopment: bool
    is_broadcast: bool
    expiration: str

class GetExtensionBitsProductsResponse(Utils.ResponseBaseClass):
        def __init__(self) -> None:
            super().__init__(ExtensionProduct)

class UpdateExtensionBitsProductRequest(Utils.RequestBaseClass):
    requestType = Utils.HTTPMethod.PUT
    scope = None
    authorization = Utils.AuthRequired.CLIENT
    endPoint ="/bits/extensions"
    def __init__(self, sku: str, cost: ExtensionCost, display_name: str, in_development: Optional[bool]=None, is_broadcast: Optional[bool]=None, expiration: Optional[str]=None) -> None:
        """
        __init__ used to get information about extensions installed by a specified user.

        usage: GetExtensionsRequest(extension_id, extension_version)

        :param sku: The identifier for the product data to be updated. This is the same as the SKU specified in the request.
        :type sku: str
        :param cost: The cost object for the product.
        :type cost: ExtensionCost
        :param display_name: The display name of the product.
        :type display_name: str
        :param in_development: Indicates if the product is in development.
        :type in_development: Optional[bool], optional
        :param is_broadcast: Indicates if the product is a broadcast.
        :type is_broadcast: Optional[bool], optional
        :param expiration: The expiration date of the product, in RFC 3339 format. If the product never expires, this is null.
        :type expiration: Optional[str], optional
        """
        self.sku = sku
        self.cost = cost
        self.display_name = display_name
        self.in_development = in_development
        self.is_broadcast = is_broadcast
        self.expiration = expiration
        super().__init__()

    

class UpdateExtensionBitsProductResponse(Utils.ResponseBaseClass):
        def __init__(self) -> None:
            super().__init__(ExtensionProduct)