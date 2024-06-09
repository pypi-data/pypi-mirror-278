from http import HTTPStatus
from aiohttp import ClientResponse, http_exceptions
from datetime import datetime
from typing import Callable, List, Optional
from Twitch.API.Exceptions import (
    TwitchApiBadGateway,
    TwitchApiBadRequstException,
    TwitchApiGatewayTimeout,
    TwitchApiInternalServerError, 
    TwitchApiNotFoundException,
    TwitchApiServiceUnavailable, 
    TwitchApiTooManyRequestsException, 
    TwitchApiUnauthorizedException,
    TwitchApiIvalidUserScope)
from Twitch.API.Resources.Chat import ChatSettingsItem
from Twitch.API.Resources.Users import ExtensionItem
from Twitch.API.Resources.Utils import pagenation, dateRange, RequestBaseClass, ResponseBaseClass
from Twitch.API.Resources import *
from Twitch.API._ApiRequest import APIRequest
from Twitch.API.Resources import Utils
import urllib

class Credentials:
    def __init__(self, id: str, OauthToken: str, scopes: list) -> None:
        """
        Credentials class used to store client and user credentials
        
        :param id: client id
        :type id: str
        :param OauthToken: Oauth token
        :type OauthToken: str
        :param scopes: list of scopes
        :type scopes: list
        """
        self.id = id
        self.Oauth = OauthToken
        self.scopes = scopes

class twitchAPI:
    def __init__(self, clientCreds: Credentials, userCreds: Credentials) -> None:
        """
        Twitch API class used to make requests to the twitch API

        :param clientCreds: client credentials
        :type clientCreds: Credentials
        :param userCreds: user credentials
        :type userCreds: Credentials
        """

        self.APIconnector = APIRequest("https://api.twitch.tv/helix")
        
        self._credentials:dict[Utils.AuthRequired, Credentials] = {
            Utils.AuthRequired.CLIENT : clientCreds,
            Utils.AuthRequired.USER : userCreds,
        }
    

        self._APIReqestFailedExcptions: dict[HTTPStatus, Exception] = {
            HTTPStatus.BAD_REQUEST : TwitchApiBadRequstException,
            HTTPStatus.UNAUTHORIZED : TwitchApiUnauthorizedException,
            HTTPStatus.NOT_FOUND : TwitchApiNotFoundException,
            HTTPStatus.TOO_MANY_REQUESTS : TwitchApiTooManyRequestsException,
            HTTPStatus.INTERNAL_SERVER_ERROR : TwitchApiInternalServerError,
            HTTPStatus.BAD_GATEWAY : TwitchApiBadGateway,
            HTTPStatus.SERVICE_UNAVAILABLE : TwitchApiServiceUnavailable,
            HTTPStatus.GATEWAY_TIMEOUT : TwitchApiGatewayTimeout,
        }

        self._ApiRequestSuccess: list[HTTPStatus] = [
            HTTPStatus.OK,
            HTTPStatus.ACCEPTED,
            HTTPStatus.NO_CONTENT,
            HTTPStatus.CREATED,
        ]

    @property
    def _user(self) -> Credentials:
        return self._credentials[Utils.AuthRequired.USER]
    
    @property
    def _client(self) -> Credentials:
        return self._credentials[Utils.AuthRequired.CLIENT]
    
    def _getParams(self, request: RequestBaseClass) -> List[tuple[str, str]]:
        """
        _getParams gathers all request class properies and turns them into a list of tuples contains key/value pairs if variables are not None

        :param request: request class to get properties from
        :type request: RequestBaseClass
        :return: list of tuples containing key/value pairs of request class properties
        :rtype: List[tuple[str, str]]
        """
        params = list()
        for key, value in request.__dict__.items():
            if value is not None:
                if isinstance(value, list):
                    for item in value:
                        params.append((key, item))
                else:
                    params.append((key,value))
        return params

    async def _twitchAPICall(self, request: RequestBaseClass, response: ResponseBaseClass, **kwargs) -> None:
        """
        Sends a request to the twitch API and fills the response object with the returned data

        :param request: request class to get propertie
        
        :return: None
        """
        if request.authorization == Utils.AuthRequired.USER and request.scope is not None and request.scope not in self._user.scopes:
            raise TwitchApiIvalidUserScope("User doesn't have required scope!")    
        
        headers = {
            #set Authorization token based on api call required authorization
            'Authorization': f'Bearer {self._credentials[request.authorization].Oauth}',
            'Client-Id': self._client.id,
        }

        APIresponse: ClientResponse = await self.APIconnector.request(request.endPoint, request.requestType, headers=headers, params=self._getParams(request))
        if APIresponse.status in self._ApiRequestFailedExcptions:
            raise self._APIReqestFailedExcptions[APIresponse.status](await APIresponse.json())
        elif APIresponse.status in self._ApiRequestSuccess:
            response.raw = await APIresponse.json()
            response.status = APIresponse.status
            for key, value in response.raw.items():
                    response.__setattr__(key, value)
        else:
            raise Exception("Unknown API response status")
        return 
    
       
    ############################### API CALLS #########################################


    async def StartCommercial(self, length: int) -> StartCommercialRepsonse:
        """
        StartCommercial Starts a commercial on the specified channel.

            NOTE: Only partners and affiliates may run commercials and they must be streaming live at the time.

            NOTE: Only the broadcaster may start a commercial; the broadcaster’s editors and moderators may not start commercials on behalf of the broadcaster.

            Authorization
                Requires a user access token that includes the channel:edit:commercial scope.

        :param length: The length of the commercial to run, in seconds. Twitch tries to serve a commercial that's the requested length, but it may be shorter or longer. The maximum length you should request is 180 seconds.
        :type length: int
        :return: data object contains the status of your start commercial request.
        :rtype: StartCommercialRepsonse
               data:	Object[]	An list that contains a single object with the status of your start commercial request.
               {
                        length:	Integer	The length of the commercial you requested. If you request a commercial that’s 
                                longer than 180 seconds, the API uses 180 seconds.
                        message:	String	A message that indicates whether Twitch was able to serve an ad.
                        retry_after:	Integer	The number of seconds you must wait before running another commercial.
                }
        """
        request = StartCommercialRequest(self._user.id, length)
        response = StartCommercialRepsonse()
        await self._twitchAPICall(request, response)
        return response

    async def GetExtensionAnalytics(self,extension_id: Optional[str]= None, 
                type: Optional[str]= None,
                started_at: Optional[datetime] = None,
                ended_at: Optional[datetime] = None,
                first: Optional[int] = None,
                after: Optional[str] = None) -> GetExtensionAnalyticsResponse:
        """
        GetExtensionAnalytics gets a URL that extension developers can use to download analytics reports (CSV files) for their extensions. The URL is valid for 5 minutes. Currently, only one URL can be generated at a time.
        
        Required Authentication: User access token with analytics:read:extensions scope.
    
        :param extension_id: Extentions client ID, if specified returns analytics for that extention, if not returns analytics for all extensions the user owns, defaults to None 
        :type extension_id: Optional[str], optional
        :param type: the type of report to generate, possible values: overview_v2
        :type type: Optional[str], optional
        :param started_at: the report start date in RFC3339 format, defaults to None
        :type started_at: Optional[datetime], optional
        :param ended_at: the report end date in RFC3339 format, defaults to None
        :type ended_at: Optional[datetime], optional
        :param first:  the number of objects to return, maximum 100, api default 20, defaults to None
        :param after: the cursor for the next page of data, defaults to None    
        :type after: Optional[str], optional
        :return: data object contains  report URLs
        :rtype: GetExtensionAnalyticsResponse
            data: Object[]	An array of objects that contain the report URLs.
            {
                extension_id:	String	The extension ID.
                url:	String	The URL to download the report.
                type:	String	The type of report.
                date_range:	Object	An object that contains the start and end dates for the report.
                {
                    started_at:	String	The start date for the report.
                    ended_at:	String	The end date for the report.
                }   
            }
            Pagination: Cursor based pagination
        """
        request = GetExtensionAnalyticsRequest(extension_id, type, started_at, ended_at, first, after)       
        response = GetExtensionAnalyticsResponse()
        await self._twitchAPICall(request, response)
        return response
    
    async def GetGameAnalytics(self,                 
                 game_id: Optional[str] = None,
                 type: Optional[str]= None,
                 started_at: Optional[datetime] = None,
                 ended_at: Optional[datetime] = None,
                 first: Optional[int] = None,
                 after: Optional[str] = None ) -> GetGameAnalyticsResponse:
        
        """
        GetGameAnalytics  Gets a URL that game developers can use to download analytics reports (CSV files) for their games. The URL is valid for 5 minutes. Currently, only one URL can be generated at a time.

        Required Authentication: User access token with analytics:read:games scope.

        :param game_id: when specified returns analytics for that game, if not returns analytics for all games the user owns, defaults to None
        :type game_id: Optional[str], optional
        :param type: the type of report to generate, possible values: overview_v2
        :type type: Optional[str], optional
        :param started_at:  the report start date in RFC3339 format, defaults to None
        :type started_at: Optional[datetime], optional
        :param ended_at: the report end date in RFC3339 format, defaults to None
        :type ended_at: Optional[datetime], optional
        :param first: the number of objects to return, maximum 100, api default 20, defaults to None    
        :type first: Optional[int], optional
        :param after: the cursor for the next page of data, defaults to None
        :type after: Optional[str], optional
        :return: data object contains  report URLs
        :rtype: GetGameAnalyticsResponse
            data: Object[]	An array of objects that contain the report URLs.
            {
                game_id:	String	The game ID.
                url:	String	The URL to download the report.
                type:	String	The type of report.
                date_range:	Object	An object that contains the start and end dates for the report.
                {
                    started_at:	String	The start date for the report.
                    ended_at:	String	The end date for the report.
                }
            }
            Pagination: Cursor based pagination
            
        """
        
        request = GetGameAnalyticsRequest(game_id, type, started_at, ended_at, first, after)
        response = GetGameAnalyticsResponse()
        await self._twitchAPICall(request, response)
        return response

    async def GetBitsLeaderboard(self, count:Optional[int]=None, 
                                 period: Optional[str]=None, 
                                 started_at: Optional[datetime]=None, 
                                 user_id: Optional[str]=None) -> GetBitsLeaderboardResponse:
        """
        GetBitsLeaderboard  Gets a ranked list of Bits leaderboard information for an authorized broadcaster.

        Required Authentication: User access token with bits:read scope.

        :param count: number of results to be returned, defaults to None
        :type count: Optional[int], optional
        :param period: time period over which data is aggregated (PST time zone); "day" (default) or "week", defaults to None
        :type period: Optional[str], optional
        :param started_at: timestamp for the period over which the returned data is aggregated; current period if not specified, defaults to None
        :type started_at: Optional[datetime], optional
        :param user_id: ID of the user whose results are returned; user_id must match the user_id in the auth token, defaults to None
        :type user_id: Optional[str], optional
        :return: data object containing leaderboard information
        :rtype: GetBitsLeaderboardResponse
            data: Object[]	An array of objects that contain leaderboard information.
            {
                user_id:	String	The user ID of the user (viewer) in the leaderboard entry.
                user_login:	String	The user login of the user (viewer) in the leaderboard entry.
                user_name:	String	The display name of the user (viewer) in the leaderboard entry.
                rank:	Integer	The rank of the user in the leaderboard.
                score:	Integer	The score of the user in the leaderboard.
            }
        """
        request = GetBitsLeaderboardRequest(count, period, started_at, user_id)
        response = GetBitsLeaderboardResponse()
        await self._twitchAPICall(request, response)
        return response

    async def GetCheermotes(self, broadcaster_id: Optional[str] = None) -> GetCheermotesResponse:
        """
        GetCheermotes Gets all available cheermotes, animated emotes to which viewers can assign Bits, to cheer in chat.

        leave broadcaster_id blank to get global cheermotes.

        :param broadcaster_id: get broadcaster specific cheermotes, defaults to None
        :type broadcaster_id: Optional[str], optional
        :return: data object containing all cheermotes
        :rtype: GetCheermotesResponse

            data: Object[]	An array of objects that contain cheermote information.
            {
                prefix:	String	The prefix used to cheer with this emote.
                tiers:	Object[]	An array of objects that contain information about the various tiers of cheermotes.
                {
                    min_bits:	Integer	The minimum number of bits needed to trigger the associated emote tier.
                    id:	String	The ID of the emote tier.
                    color:	String	The color associated with the bits of that tier.
                    images:	Object	An object that contains URLs for the cheermote images scaled to different sizes.
                    {
                        dark:	Object	An object that contains URLs for the cheermote images with a dark color scheme scaled to different sizes.
                        {
                            animated:	Object	An object that contains URLs for the animated cheermote images scaled to different sizes.
                            {
                                "1":	String	The URL for the 1x animated cheermote.
                                "1.5":	String	The URL for the 1.5x animated cheermote.
                                "2":	String	The URL for the 2x animated cheermote.
                                "3":	String	The URL for the 3x animated cheermote.
                                "4":	String	The URL for the 4x animated cheermote.
                            }
                            static:	Object	An object that contains URLs for the static cheermote images scaled to different sizes.
                            {
                                "1":	String	The URL for the 1x static cheermote.
                                "1.5":	String	The URL for the 1.5x static cheermote.
                                "2":	String	The URL for the 2x static cheermote.
                                "3":	String	The URL for the 3x static cheermote.
                                "4":	String	The URL for the 4x static cheermote.
                            }   
                        }
                        light:	Object	An object that contains URLs for the cheermote images with a light color scheme scaled to different sizes.
                        {
                            animated:	Object	An object that contains URLs for the animated cheermote images scaled to different sizes.
                            {
                                "1":	String	The URL for the 1x animated cheermote.
                                "1.5":	String	The URL for the 1.5x animated cheermote.
                                "2":	String	The URL for the 2x animated cheermote.
                                "3":	String	The URL for the 3x animated cheermote.
                                "4":	String	The URL for the 4x animated cheermote.
                            }
                            static:	Object	An object that contains URLs for the static cheermote images scaled to different sizes.
                            {
                                "1":	String	The URL for the 1x static cheermote.
                                "1.5":	String	The URL for the 1.5x static cheermote.
                                "2":	String	The URL for the 2x static cheermote.
                                "3":	String	The URL for the 3x static cheermote.
                                "4":	String	The URL for the 4x static cheermote.
                            }
                        }
                    }
                    can_cheer:	Boolean	Indicates whether the emote tier can be used to cheer with Bits.
                    show_in_bits_card:	Boolean	Indicates whether the emote tier is shown in the Bits card.
                }
                type:	String	The type of emote.
                order:	Integer	The order of the emote in the list of emotes.
                last_updated:	String	The date when the emote was last updated.
                is_charitable:	Boolean	Indicates whether the emote is a charitable emote.
            }
        """
        request = GetCheermotesRequest(broadcaster_id)
        response = GetCheermotesResponse()
        await self._twitchAPICall(request, response)
        return response

    async def GetExtensionTransactions(self, extension_id:str, 
                                       id: Optional[str]=None, 
                                       first: Optional[int]=None, 
                                       after: Optional[str]=None) -> GetExtensionTransactionsResponse:
        """
        GetExtensionTransactions Gets a URL that extension developers can use to download a CSV file with a report of their extension transactions data. The URL is valid for 5 minutes. Currently, only one URL can be generated at a time.

        Required Authentication: App access token with analytics:read:extensions scope.

        :param extension_id: ID of the extension whose transactions are being fetched.
        :type extension_id: str
        :param id: ID of the transaction being fetched, defaults to None
        :type id: Optional[str], optional
        :param first: number of objects to return, defaults to None
        :type first: Optional[int], optional
        :param after: cursor for forward pagination, defaults to None
        :type after: Optional[str], optional
        :return: data object containing transaction information
        :rtype: GetExtensionTransactionsResponse
        """
        request = GetExtensionTransactionsRequest(extension_id, id, first, after)
        response = GetExtensionTransactionsResponse()
        await self._twitchAPICall(request, response)
        return response

    async def GetChannelInformation(self, broadcaster_id: List[str]) -> GetChannelInformationResponse:
        """
        GetChannelInformation Gets information about a specified Twitch channel.

        Required Authentication: Uses Client access token to search broadcaster ids  .

        :param broadcaster_id: ID of the broadcaster whose channel is being queried.
        :type broadcaster_id: str
        :return: data object containing channel information
        :rtype: GetChannelInformationResponse      
        """

        request = GetChannelInformationRequest(broadcaster_id)
        response = GetChannelInformationResponse()
        await self._twitchAPICall(request, response)
        return response
    
    async def GetChannelInformationOfUser(self) -> GetChannelInformationResponse:
        """
        GetChannelInformationAsUser Gets information about a specified Twitch channel.

        Required Authentication: User access token with channel:read:subscriptions scope.

        :param broadcaster_id: ID of the broadcaster whose channel is being queried.
        :type broadcaster_id: str
        :return: data object containing channel information
        :rtype: GetChannelInformationResponse      
        """
        request = GetChannelInformationRequest(self._user.id, True)
        response = GetChannelInformationResponse()
        await self._twitchAPICall(request, response)
        return response

    async def ModifyChannelInformation(self, title: Optional[str]=None, 
                                       delay: Optional[int]=None, 
                                       tags: Optional[list[str]]=None) -> ModifyChannelInformationResponse:
        """
        ModifyChannelInformation Modifies channel information for users. Channel information includes metadata, stream title, and stream delay.

        Required Authentication: User access token with channel:manage:broadcast scope.

        :param title: channel title, defaults to None
        :type title: Optional[str], optional
        :param delay: channel delay, defaults to None
        :type delay: Optional[int], optional
        :param tags: array of tags, defaults to None
        :type tags: Optional[list[str]], optional
        :return: data object containing channel information
        :rtype: ModifyChannelInformationResponse
        """ 
        request = ModifyChannelInformationRequest(self._user.id, title, delay, tags)
        response = GetExtensionTransactionsResponse()
        await self._twitchAPICall(request, response)
        return response
        
    async def GetChannelEditors(self) -> GetChannelEditorsResponse:
        """
        GetChannelEditors Gets a list of users who are editors for a specific channel.

        Required Authentication: User access token with channel:read:editors scope.

        :return: data object containing channel editor information
        :rtype: GetChannelEditorsResponse
        """
        request = GetChannelEditorsRequest(self._user.id)
        response = GetChannelEditorsResponse()
        await self._twitchAPICall(request, response)
        return response
    
    async def GetFollowedChannels(self, broadcaster_id: Optional[str]=None, 
                                  first:Optional[int]=None, 
                                  after: Optional[str]=None) -> GetFollowedChannelsResponse:
        """
        GetFollowedChannels Gets a list of all channels that the authenticated user follows.

        Required Authentication: User access token with user:read:follows scope.

        :param broadcaster_id: ID of the broadcaster whose channel is being queried, defaults to None
        :type broadcaster_id: Optional[str], optional
        :param first: number of objects to return, defaults to None
        :type first: Optional[int], optional
        :param after: cursor for forward pagination, defaults to None
        :type after: Optional[str], optional
        :return: data object containing channel information
        :rtype: GetFollowedChannelsResponse
        """
        request = GetFollowedChannelsRequest(self._user.id, broadcaster_id, first, after)
        response = GetFollowedChannelsResponse()
        await self._twitchAPICall(request, response)
        return response
    
    async def GetChannelFollowers(self, broadcaster_id: str,
                                    user_id: Optional[str]=None,
                                    first: Optional[int]=None,
                                    after: Optional[str]=None,
                                    from_id: Optional[str]=None) -> GetChannelFollowersResponse:
        """
        GetChannelFollowers Gets a list of users who follow a specified channel, sorted by the date when they started following the channel (newest first, unless specified otherwise).

        Required Authentication: User access token with moderator:read:follows scope.

        :param broadcaster_id: ID of the broadcaster whose channel is being queried.
        :type broadcaster_id: str
        :param user_id: ID of the user whose follows are being queried, defaults to None
        :type user_id: Optional[str], optional
        :param first: number of objects to return, defaults to None
        :type first: Optional[int], optional
        :param after: cursor for forward pagination, defaults to None
        :type after: Optional[str], optional
        :param from_id: ID of the user who is requesting the information, defaults to None
        :type from_id: Optional[str], optional
        :return: data object containing channel follower information
        :rtype: GetChannelFollowersResponse
        """
        request = GetChannelFollowersRequest(broadcaster_id, user_id, first, after, from_id)
        response = GetChannelFollowersResponse()
        await self._twitchAPICall(request, response)
        return response
    

    async def CreateCustomRewards(self, title: str, 
                                cost: int, 
                                prompt: Optional[str]=None, 
                                is_enabled: Optional[bool]=None,
                                background_color: Optional[str]=None,
                                is_user_input_required: Optional[bool]=None,
                                is_max_per_stream_enabled: Optional[bool]=None,
                                max_per_stream: Optional[int]=None,
                                is_max_per_user_per_stream_enabled: Optional[bool]=None,
                                max_per_user_per_stream: Optional[int]=None,
                                is_global_cooldown_enabled: Optional[bool]=None,
                                global_cooldown_seconds: Optional[int]=None,
                                should_redemptions_skip_request_queue: Optional[bool]=None) -> CreateCustomRewardsResponse:
        """
        CreateCustomRewards Creates a custom channel points reward.

        Required Authentication: User access token with channel:manage:redemptions scope.

        :param title: title of the reward
        :type title: str
        :param cost: cost of the reward
        :type cost: int
        :param prompt: prompt for the reward, defaults to None
        :type prompt: Optional[str], optional
        :param is_enabled: whether the reward is enabled, defaults to None
        :type is_enabled: Optional[bool], optional
        :param background_color: background color of the reward, defaults to None
        :type background_color: Optional[str], optional
        :param is_user_input_required: whether user input is required, defaults to None
        :type is_user_input_required: Optional[bool], optional
        :param is_max_per_stream_enabled: whether max per stream is enabled, defaults to None
        :type is_max_per_stream_enabled: Optional[bool], optional
        :param max_per_stream: max per stream, defaults to None
        :type max_per_stream: Optional[int], optional
        :param is_max_per_user_per_stream_enabled: whether max per user per stream is enabled, defaults to None
        :type is_max_per_user_per_stream_enabled: Optional[bool], optional
        :param max_per_user_per_stream: max per user per stream, defaults to None
        :type max_per_user_per_stream: Optional[int], optional
        :param is_global_cooldown_enabled: whether global cooldown is enabled, defaults to None
        :type is_global_cooldown_enabled: Optional[bool], optional
        :param global_cooldown_seconds: global cooldown seconds, defaults to None
        :type global_cooldown_seconds: Optional[int], optional
        :param should_redemptions_skip_request_queue: whether redemptions should skip request queue, defaults to None
        :type should_redemptions_skip_request_queue: Optional[bool], optional
        :return: data object containing reward information
        :rtype: CreateCustomRewardsResponse
        """
        
        request = CreateCustomRewardsRequest(self._user.id, 
                                             title, cost, 
                                             prompt, is_enabled, 
                                             background_color, is_user_input_required,
                                             is_max_per_stream_enabled, max_per_stream,
                                             is_max_per_user_per_stream_enabled, 
                                             max_per_user_per_stream,
                                             is_global_cooldown_enabled,
                                             global_cooldown_seconds,
                                             should_redemptions_skip_request_queue)
        
        response = CreateCustomRewardsResponse()
        await self._twitchAPICall(request, response)
        return response
    
    
    async def DeleteCustomReward(self, id: str) -> DeleteCustomRewardResponse:
        """
        DeleteCustomReward Deletes a custom channel points reward.
        
        Required Authentication: User access token with channel:manage:redemptions scope.

        :param id: ID of the reward to delete
        :type id: str
        :return: data object containing reward information
        :rtype: DeleteCustomRewardResponse
        """
        request = DeleteCustomRewardRequest(self._user.id, id)
        response = DeleteCustomRewardResponse()
        await self._twitchAPICall(request, response)
        return response
    
    async def GetCustomReward(self, id: str, only_manageable_rewards: Optional[bool]=None) -> GetCustomRewardResponse:
        """
        GetCustomReward Gets a custom channel points reward by reward ID (reward ID is returned when creating the reward).

        Required Authentication: User access token with channel:manage:redemptions scope or channel:read:redemptions scope.
        
        :param id: ID of the reward to get
        :type id: str
        :param only_manageable_rewards: whether to only return rewards managed by the client_id, default is False
        :type only_manageable_rewards: Optional[bool], optional
        :return: data object containing reward information
        :rtype: GetCustomRewardResponse
        """
        request = GetCustomRewardRequest(self._user.id, id, only_manageable_rewards)
        response = GetCustomRewardResponse()
        await self._twitchAPICall(request, response)
        return response
    
    async def GetCustomRewardRedemption(self, reward_id: str, status: str,id: str, sort: Optional[str]=None, after: Optional[str]=None, first: Optional[int]=None) -> GetCustomRewardRedemptionResponse:
        """
        GetCustomRewardRedemption Gets a custom channel points reward by reward ID (reward ID is returned when creating the reward).

        Required Authentication: User access token with channel:manage:redemptions scope or channel:read:redemptions scope.

        :param reward_id: ID of the reward to get
        :type reward_id: str
        :param status: status of redemptions to get (UNFULFILLED, FULFILLED, CANCELED), defaults to None
        :type status: Optional[str], optional
        :param id: id of redemptions to get, defaults to None
        :type id: Optional[str], optional
        :param sort: sort order of redemptions, defaults to None
        :type sort: Optional[str], optional
        :param after: cursor for forward pagination, defaults to None
        :type after: Optional[str], optional
        :param first: number of results to return, defaults to None
        :type first: Optional[int], optional
        :return: data object containing reward information
        :rtype: GetCustomRewardRedemptionResponse
        """
        request = GetCustomRewardRedemptionRequest(self._user.id, reward_id, status, id, sort, after, first)
        response = GetCustomRewardRedemptionResponse()
        await self._twitchAPICall(request, response)
        return response
    
    async def UpdateCustomReward(self, 
                                 id: str, 
                                 title: Optional[str]=None, 
                                 prompt: Optional[str]=None, 
                                 cost: Optional[int]=None, 
                                 is_enabled: Optional[bool]=None, 
                                 background_color: Optional[str]=None, 
                                 is_user_input_required: Optional[bool]=None, 
                                 is_max_per_stream_enabled: Optional[bool]=None, 
                                 max_per_stream: Optional[int]=None, 
                                 is_max_per_user_per_stream_enabled: Optional[bool]=None, 
                                 max_per_user_per_stream: Optional[int]=None, 
                                 is_global_cooldown_enabled: Optional[bool]=None, 
                                 global_cooldown_seconds: Optional[int]=None, 
                                 should_redemptions_skip_request_queue: Optional[bool]=None) -> UpdateCustomRewardResponse:
        """
        UpdateCustomReward Updates a custom channel points reward.

        Required Authentication: User access token with channel:manage:redemptions scope.

        :param id: ID of the reward to update
        :type id: str
        :param title: title of the reward, defaults to None
        :type title: Optional[str], optional
        :param prompt: prompt for the user when redeeming the reward, defaults to None
        :type prompt: Optional[str], optional
        :param cost: cost of the reward, defaults to None
        :type cost: Optional[int], optional
        :param is_enabled: whether the reward is enabled or not, defaults to None
        :type is_enabled: Optional[bool], optional
        :param background_color: background color of the reward, defaults to None
        :type background_color: Optional[str], optional
        :param is_user_input_required: whether user input is required when redeeming the reward, defaults to None
        :type is_user_input_required: Optional[bool], optional
        :param is_max_per_stream_enabled: whether the reward is enabled for the current stream, defaults to None
        :type is_max_per_stream_enabled: Optional[bool], optional
        :param max_per_stream: max number of redemptions per stream, defaults to None
        :type max_per_stream: Optional[int], optional
        :param is_max_per_user_per_stream_enabled: whether the reward is enabled per user per stream, defaults to None
        :type is_max_per_user_per_stream_enabled: Optional[bool], optional
        :param max_per_user_per_stream: max number of redemptions per stream per user, defaults to None
        :type max_per_user_per_stream: Optional[int], optional
        :param is_global_cooldown_enabled: whether the cooldown is enabled, defaults to None
        :type is_global_cooldown_enabled: Optional[bool], optional
        :param global_cooldown_seconds: cooldown in seconds, defaults to None
        :type global_cooldown_seconds: Optional[int], optional
        :param should_redemptions_skip_request_queue: whether redemptions should be skipped, defaults to None
        :type should_redemptions_skip_request_queue: Optional[bool], optional
        :return: data object containing reward information
        :rtype: UpdateCustomRewardResponse
        """
        request = UpdateCustomRewardRequest(self._user.id, 
                                            id, 
                                            title, 
                                            prompt,
                                            cost, 
                                            is_enabled, 
                                            background_color, 
                                            is_user_input_required, 
                                            is_max_per_stream_enabled, 
                                            max_per_stream, is_max_per_user_per_stream_enabled, 
                                            max_per_user_per_stream, 
                                            is_global_cooldown_enabled, 
                                            global_cooldown_seconds, 
                                            should_redemptions_skip_request_queue)
        response = UpdateCustomRewardResponse()
        await self._twitchAPICall(request, response)
        return response

    async def UpdateRedemptionStatus(self, id, reward_id, status) -> UpdateRedemptionStatusResponse:
        """
        UpdateRedemptionStatus Updates the status of Custom Reward Redemption objects on a channel that are in the UNFULFILLED status.

        Required Authentication: User access token with channel:manage:redemptions scope.

        :param id: ID of the redemption to update
        :type id: str
        :param reward_id: ID of the reward to update
        :type reward_id: str
        :param status: status of the redemption to update (UNFULFILLED, FULFILLED, CANCELED)
        :type status: str
        :return: data object containing reward information
        :rtype: UpdateRedemptionStatusResponse
        """
        request = UpdateRedemptionStatusRequest(id, self._user.id, reward_id, status)
        request = UpdateRedemptionStatusRequest()
        response = UpdateRedemptionStatusResponse()
        await self._twitchAPICall(request, response)
        return response
    
    async def GetCharityCampaign(self) -> GetCharityCampaignResponse:
        """
        GetCharityCampaign Gets the currently active charity campaign on a channel.

        Required Authentication: App access token with channel:read:redemptions scope.

        :return: data object containing reward information
        :rtype: GetCharityCampaignResponse
        """
        request = GetCharityCampaignRequest(self._user.id)
        response = GetCharityCampaignResponse()
        await self._twitchAPICall(request, response)
        return response
    
    async def GetCharityCampaignDonations(self,first: Optional[int]=None, after: Optional[str]=None) -> GetCharityCampaignDonationsResponse:
        """
        GetCharityCampaignDonations Gets a list of donations made to a specified charity campaign.

        Required Authentication: App access token with channel:read:redemptions scope.

        :param first: Maximum number of objects to return. Maximum: 100. Default: 20., defaults to None
        :type first: Optional[int], optional
        :param after: Cursor for forward pagination: tells the server where to start fetching the next set of results, in a multi-page response., defaults to None
        :type after: Optional[str], optional
        :return: data object containing reward information
        :rtype: GetCharityCampaignDonationsResponse
        """
        request = GetCharityCampaignDonationsRequest(self._user.id, first, after)
        response = GetCharityCampaignDonationsResponse()
        await self._twitchAPICall(request, response)
        return response
    
    async def GetChatters(self, broadcaster_id: str, moderator_id: str, first: Optional[int]=None, after: Optional[str]=None) -> GetChattersResponse:
        """
        GetChatters Gets all chatters in a specified channel. Chatters are users who have sent a message in the channel or are currently in the channel.

        Required Authentication: App access token with channel:read:redemptions scope.

        :param broadcaster_id: ID of the broadcaster whose channel is being queried.

        :type broadcaster_id: str
        :param moderation_id: ID of the user who is requesting the information. Must match user_id in the auth token if it is provided., defaults to None
        :type moderation_id: Optional[str], optional
        :param first: Maximum number of objects to return. Maximum: 100. Default: 20., defaults to None
        :type first: Optional[int], optional
        :param after: Cursor for forward pagination: tells the server where to start fetching the next set of results, in a multi-page response., defaults to None
        :type after: Optional[str], optional
        :return: data object containing reward information
        :rtype: GetChattersResponse
        """
        request = GetChattersRequest(broadcaster_id, moderator_id, first, after)
        response = GetChattersResponse()
        await self._twitchAPICall(request, response)
        return response
    
    async def GetChannelEmotes(self, broadcaster_id: str) -> GetChannelEmotesResponse:
        """
        GetChannelEmotes Gets all custom chat emotes (not including those from BetterTTV and FrankerFaceZ) for a specified channel. Custom chat emotes are channel-specific emoticons that users can post in chat.

        Required Authentication: None

        :param broadcaster_id: ID of the broadcaster whose channel is being queried.
        :type broadcaster_id: str
        :return: data object containing reward information
        :rtype: GetChannelEmotesResponse
        """
        request = GetChannelEmotesRequest(broadcaster_id)
        response = GetChannelEmotesResponse()
        await self._twitchAPICall(request, response)
        return response
    
    async def GetGlobalEmotes(self) -> GetGlobalEmotesResponse:
        """
        GetGlobalEmotes Gets all global emotes. Global emotes are Twitch-specific emoticons that any user (Twitch Affiliate or Twitch Partner) can use in Twitch chat.

        Required Authentication: None

        :return: data object containing reward information
        :rtype: GetGlobalEmotesResponse
        """
        request = GetGlobalEmotesRequest()
        response = GetGlobalEmotesResponse()
        await self._twitchAPICall(request, response)
        return response
    
    async def GetEmoteSets(self,emote_set_id: str) -> GetEmoteSetsResponse:
        """
        GetEmoteSets Gets all emote sets (emoticon packs) available to the channel.

        Required Authentication: None

        :param emote_set_id: ID of the emote set.
        :type emote_set_id: str
        :return: data object containing reward information      
        :rtype: GetEmoteSetsResponse
        """
        request = GetEmoteSetsRequest(emote_set_id)
        response = GetEmoteSetsResponse()
        await self._twitchAPICall(request, response)
        return response
    
    async def GetChannelChatBadges(self, broadcaster_id: str) -> GetChannelChatBadgesResponse:
        """
        GetChannelChatBadges Gets a list of chat badges that can be used in the specified channel’s chat.

        Required Authentication: None

        :param broadcaster_id: ID of the broadcaster whose channel is being queried.
        :type broadcaster_id: str
        :return: data object containing chat badge information
        :rtype: GetChannelChatBadgesResponse
        """
        request = GetChannelChatBadgesRequest(broadcaster_id)
        response = GetChannelChatBadgesResponse()
        await self._twitchAPICall(request, response)
        return response
    
    async def GetGlobalChatBadges(self) -> GetGlobalChatBadgesResponse:
        """
        GetGlobalChatBadges Gets a list of global chat badges.

        Required Authentication: None

        :return: data object containing chat badge information
        :rtype: GetGlobalChatBadgesResponse
        """
        request = GetGlobalChatBadgesRequest()
        response = GetGlobalChatBadgesResponse()
        await self._twitchAPICall(request, response)
        return response
    
    async def GetChatSettings(self, broadcaster_id: str, moderator_id: Optional[str]=None) -> GetChatSettingsResponse:
        """
        GetChatSettings Gets a specified channel’s chat settings. Chat settings are returned in the chat_settings object.

        Required Authentication: None

        :param broadcaster_id: ID of the broadcaster whose channel is being queried.
        :type broadcaster_id: str
        :param moderator_id: ID of the user who is requesting the information. Must match user_id in the auth token if it is provided., defaults to None
        :type moderator_id: Optional[str], optional
        :return: data object containing chat settings information
        :rtype: GetChatSettingsResponse
        """
        request = GetChatSettingsRequest(broadcaster_id, moderator_id)
        response = GetChatSettingsResponse()
        await self._twitchAPICall(request, response)
        return response
    
    async def UpdateChatSettings(self, broadcaster_id: str, moderator_id: str, emote_mode: Optional[bool]=None, followers_mode: Optional[bool]=None, 
                                 follower_mode_duration: Optional[int]=None, slow_mode_wait_time: Optional[int]=None, sub_mode: Optional[bool]=None,
                                 subscribers_mode: Optional[bool]=None, unique_chat_mode: Optional[bool]=None, non_moderator_chat_delay: Optional[int]=None, 
                                 non_moderator_chat_delay_duration: Optional[int]=None) -> UpdateChatSettingsResponse:
        """
        UpdateChatSettings Updates a specified channel’s chat settings. Chat settings are returned in the chat_settings object.

        Required Authentication: User access token with channel:manage:broadcast scope.

        :param broadcaster_id: ID of the broadcaster whose channel is being queried.
        :type broadcaster_id: str
        :param moderator_id: ID of the user who is requesting the information. Must match user_id in the auth token if it is provided., defaults to None
        :type moderator_id: Optional[str], optional
        :param emote_mode: Whether emote-only mode is enabled. Valid values: true, false, defaults to None
        :type emote_mode: Optional[bool], optional
        :param followers_mode: Whether followers-only mode is enabled. Valid values: true, false, defaults to None
        :type followers_mode: Optional[bool], optional
        :param follower_mode_duration: Duration in minutes that followers-only mode should last. Valid values: 0 - 3 months (0 - 129600 minutes). Defaults to 0., defaults to None
        :type follower_mode_duration: Optional[int], optional
        :param slow_mode_wait_time: Duration in seconds that slow mode should last. Valid values: 0 - 1200. Defaults to 0., defaults to None
        :type slow_mode_wait_time: Optional[int], optional
        :param sub_mode: Whether sub-only mode is enabled. Valid values: true, false, defaults to None
        :type sub_mode: Optional[bool], optional
        :param subscribers_mode: Whether sub-only mode is enabled. Valid values: true, false, defaults to None
        :type subscribers_mode: Optional[bool], optional
        :param unique_chat_mode: Whether unique chat is enabled. Valid values: true, false, defaults to None
        :type unique_chat_mode: Optional[bool], optional
        :param non_moderator_chat_delay: Duration in seconds that non-moderators should be prevented from sending messages. Valid values: 0 - 1200. Defaults to 0., defaults to None
        :type non_moderator_chat_delay: Optional[int], optional
        :param non_moderator_chat_delay_duration: Duration in seconds that non-moderators should be prevented from sending messages. Valid values: 0 - 1200. Defaults to 0., defaults to None
        :type non_moderator_chat_delay_duration: Optional[int], optional
        :return: data object containing chat settings information
        :rtype: UpdateChatSettingsResponse
        """

        
        request = UpdateChatSettingsRequest(broadcaster_id, moderator_id, 
                                            emote_mode, followers_mode, follower_mode_duration, 
                                            slow_mode_wait_time, sub_mode, subscribers_mode,
                                            unique_chat_mode, non_moderator_chat_delay, 
                                            non_moderator_chat_delay_duration)
        response = UpdateChatSettingsResponse()
        await self._twitchAPICall(request, response)
        return response
    
    async def SendChatAnnouncement(self, broadcaster_id: str, moderator_id: str, message: str, color: Optional[str]=None) -> SendChatAnnouncementResponse:
        """
        SendChatAnnouncement Sends a chat message, which is visible to users in all Twitch channels.

        Required Authentication: User access token with moderator.manage.announcements scope.

        :param broadcaster_id: ID of the broadcaster whose channel is being queried.
        :type broadcaster_id: str
        :param moderator_id: ID of the user who is requesting the information. Must match user_id in the auth token if it is provided., defaults to None
        :type moderator_id: Optional[str], optional
        :param message: message to send
        :type message: str
        :param color: color of the message, defaults to None
        :type color: Optional[str], optional
        :return: data object containing chat settings information
        :rtype: SendChatAnnouncementResponse
        """
        request = SendChatAnnouncementRequest(broadcaster_id, moderator_id, message, color)
        response = SendChatAnnouncementResponse()
        await self._twitchAPICall(request, response)
        return response
    
    async def SendaShoutout(self, from_broadcaster_id: str, to_broadcaster_id: str, moderator_id: str) -> SendaShoutoutResponse:
        """
        SendaShoutout Sends a chat message, which is visible to users in all Twitch channels.

        Required Authentication: User access token with moderator.manage.shoutouts scope.

        :param from_broadcaster_id: ID of the broadcaster sending the shoutout.
        :type from_broadcaster_id: str
        :param to_broadcaster_id: ID of the broadcaster receiving the shoutout.
        :type to_broadcaster_id: str
        :param moderator_id: ID of the user who is requesting the information. Must match user_id in the auth token if it is provided., defaults to None
        :type moderator_id: Optional[str], optional
        :return: data object containing chat settings information
        :rtype: SendaShoutoutResponse
        """

        request = SendaShoutoutRequest(from_broadcaster_id, to_broadcaster_id, moderator_id)
        response = SendaShoutoutResponse()
        await self._twitchAPICall(request, response)
        return response
    
    async def GetUserChatColor(self, user_id: List[str]) -> GetUserChatColorResponse:
        """
        GetUserChatColor Gets the chat color for a specified user.

        Required Authentication: None

        :param user_id: ID of the broadcaster whose channel is being queried.
        :type user_id: str
        :return: data object containing chat settings information
        :rtype: GetUserChatColorResponse
        """
        request = GetUserChatColorRequest(user_id)
        response = GetUserChatColorResponse()
        await self._twitchAPICall(request, response)
        return response
    
    async def UpdateUserChatColor(self, user_id: str, color: str) -> UpdateUserChatColorResponse:
        """
        UpdateUserChatColor Updates the chat color for a specified user.

        Required Authentication: User access token with user:manage:chat_color scope.

        :param user_id: ID of the broadcaster whose channel is being queried.
        :type user_id: str
        :param color: color of the message
        :type color: str
        :return: data object containing chat settings information
        :rtype: UpdateUserChatColorResponse
        """
        request = UpdateUserChatColorRequest(user_id, color)
        response = UpdateUserChatColorResponse()
        await self._twitchAPICall(request, response)
        return response
    
    async def CreateClip(self, broadcaster_id: str, has_delay: Optional[bool]=False) -> CreateClipResponse:
        """
        CreateClip Creates a clip programmatically. This returns both an ID and an edit URL for the new clip.

        Required Authentication: User access token with clips:edit scope.

        :param broadcaster_id: ID of the broadcaster whose channel is being queried.
        :type broadcaster_id: str
        :param has_delay: whether the clip has a delay, defaults to False
        :type has_delay: Optional[bool], optional
        :return: data object containing chat settings information
        :rtype: CreateClipResponse
        """

        request = CreateClipRequest(broadcaster_id, has_delay)
        response = CreateClipResponse()
        await self._twitchAPICall(request, response)
        return response
    
    async def GetClipsByID(self, id: List[str]) -> GetClipsResponse:
        """
        GetClipsByID Gets clip information by clip ID (one or more).

        Required Authentication: None

        :param id: ID of the broadcaster whose channel is being queried.
        :type id: str
        :return: data object containing chat settings information
        :rtype: GetClipsByIDResponse
        """
        request = GetClipsRequest(id=id)
        response = GetClipsResponse()
        await self._twitchAPICall(request, response)
        return response

    async def GetClipsByBroadcasterID(self, broadcaster_id: str | List[str], started_at: Optional[str]=None, ended_at: Optional[str]=None, after: Optional[str]=None, before: Optional[str]=None, first: Optional[int]=None) -> GetClipsResponse:
        """
        GetClipsByBroadcasterID Gets clip information for a specified broadcaster ID. This returns a set of clip objects sorted by creation date, starting with the most recent.

        Required Authentication: None

        :param broadcaster_id: ID of the broadcaster whose channel is being queried.
        :type broadcaster_id: str | List[str]
        :param started_at: Starting date/time for returned clips, in RFC3339 format. (Note that the seconds value is ignored.)
        :type started_at: str
        :param ended_at: Ending date/time for returned clips, in RFC3339 format. (Note that the seconds value is ignored.)
        :type ended_at: str
        :param after: Cursor for forward pagination: tells the server where to start fetching the next set of results, in a multi-page response., defaults to None
        :type after: Optional[str], optional
        :param before: Cursor for backward pagination: tells the server where to start fetching the next set of results, in a multi-page response., defaults to None
        :type before: Optional[str], optional
        :param first: Maximum number of objects to return. Maximum: 100. Default: 20., defaults to None
        :type first: Optional[int], optional
        :return: data object containing chat settings information
        :rtype: GetClipsByBroadcasterIDResponse
        """
        request = GetClipsRequest(broadcaster_id=broadcaster_id, started_at=started_at, ended_at=ended_at, after=after, before=before, first=first)
        response = GetClipsResponse()
        await self._twitchAPICall(request, response)
        return response
    
    async def GetClipsByGameID(self, game_id: str | List[str], started_at: Optional[str]=None, ended_at: Optional[str]=None, after: Optional[str]=None, before: Optional[str]=None, first: Optional[int]=None) -> GetClipsResponse:
        """
        GetClipsByGameID Gets clip information for a specified game ID. This returns a set of clip objects sorted by creation date, starting with the most recent.

        Required Authentication: None

        :param game_id: ID of the broadcaster whose channel is being queried.
        :type game_id: str | List[str]
        :param id: ID of the broadcaster whose channel is being queried.
        :type id: str
        :param started_at: Starting date/time for returned clips, in RFC3339 format. (Note that the seconds value is ignored.)
        :type started_at: str
        :param ended_at: Ending date/time for returned clips, in RFC3339 format. (Note that the seconds value is ignored.)
        :type ended_at: str
        :param after: Cursor for forward pagination: tells the server where to start fetching the next set of results, in a multi-page response., defaults to None
        :type after: Optional[str], optional
        :param before: Cursor for backward pagination: tells the server where to start fetching the next set of results, in a multi-page response., defaults to None
        :type before: Optional[str], optional
        :param first: Maximum number of objects to return. Maximum: 100. Default: 20., defaults to None
        :type first: Optional[int], optional
        :return: data object containing chat settings information
        :rtype: GetClipsByGameIDResponse
        """
        request = GetClipsRequest(game_id=game_id, started_at=started_at, ended_at=ended_at, after=after, before=before, first=first)
        response = GetClipsResponse()
        await self._twitchAPICall(request, response)
        return response
    
    async def GetDropsEntitlementsByID(self, id: List[str], fulfillment_status: Optional[str]=None) -> GetDropsEntitlementsResponse:
        """
        GetDropsEntitlementsByID Gets drop entitlements for a given Drops campaign ID.

        Required Authentication: User access token with drops:read scope.

        :param id: ID of the broadcaster whose channel is being queried.
        :type id: str
        :param fullfillment_status: ID of the broadcaster whose channel is being queried., defaults to None
        :type fullfillment_status: Optional[str], optional
        :return: data object containing chat settings information
        :rtype: GetDropsEntitlementsByIDResponse
        """
        request = GetDropsEntitlementsRequest(id=id, fulfillment_status=fulfillment_status)
        response = GetDropsEntitlementsResponse()
        await self._twitchAPICall(request, response)
        return response
    
    async def GetDropsEntitlementsByUser(self, user_id: str, game_id: Optional[str]=None, fulfillment_status: Optional[str]=None, after: Optional[str]=None, first: Optional[int]=None) -> GetDropsEntitlementsResponse:
        """
        GetDropsEntitlementsByUser Gets drop entitlements for a given user ID.

        Required Authentication: User access token with drops:read scope.

        :param user_id: ID of the broadcaster whose channel is being queried.
        :type user_id: str
        :param game_id: ID of the broadcaster whose channel is being queried., defaults to None
        :type game_id: Optional[str], optional
        :param fullfillment_status: ID of the broadcaster whose channel is being queried., defaults to None
        :type fullfillment_status: Optional[str], optional
        :param after: Cursor for forward pagination: tells the server where to start fetching the next set of results, in a multi-page response., defaults to None
        :type after: Optional[str], optional
        :param first: Maximum number of objects to return. Maximum: 100. Default: 20., defaults to None
        :type first: Optional[int], optional
        :return: data object containing chat settings information
        :rtype: GetDropsEntitlementsByUserResponse
        """
        request = GetDropsEntitlementsRequest(user_id=user_id, game_id=game_id, fulfillment_status=fulfillment_status, after=after, first=first)
        response = GetDropsEntitlementsResponse()
        await self._twitchAPICall(request, response)
        return response
    
    async def GetDropsEntitlementsByGame(self, game_id: str, fulfillment_status: Optional[str]=None, after: Optional[str]=None, first: Optional[int]=None) -> GetDropsEntitlementsResponse:
        """
        GetDropsEntitlementsByGame Gets drop entitlements for a given game ID.

        Required Authentication: User access token with drops:read scope.

        :param game_id: ID of the broadcaster whose channel is being queried.
        :type game_id: str
        :param after: Cursor for forward pagination: tells the server where to start fetching the next set of results, in a multi-page response., defaults to None
        :type after: Optional[str], optional
        :param first: Maximum number of objects to return. Maximum: 100. Default: 20., defaults to None
        :type first: Optional[int], optional
        :return: data object containing chat settings information
        :rtype: GetDropsEntitlementsByGameResponse
        """
        request = GetDropsEntitlementsRequest(game_id=game_id, fulfillment_status=fulfillment_status, after=after, first=first)
        response = GetDropsEntitlementsResponse()
        await self._twitchAPICall(request, response)
        return response


    async def GetDropsEntitlementsForUser(self,game_id: Optional[str|List[str]], fulfillment_status: Optional[str]=None, after: Optional[str]=None, first: Optional[int]=None) -> GetDropsEntitlementsResponse:
        """
        GetDropsEntitlementsForUser Gets drop entitlements for a given game ID.

        Required Authentication: Requires an app access token or user access token. The client ID in the access token must own the game.
        
        :param game_id: ID of the broadcaster whose channel is being queried.
        :type game_id: str
        :param after: Cursor for forward pagination: tells the server where to start fetching the next set of results, in a multi-page response., defaults to None
        :type after: Optional[str], optional
        :param first: Maximum number of objects to return. Maximum: 100. Default: 20., defaults to None
        :type first: Optional[int], optional
        :return: data object containing chat settings information
        :rtype: GetDropsEntitlementsForUserResponse
        """
        
        request = GetDropsEntitlementsRequest(game_id=game_id, fulfillment_status=fulfillment_status, after=after, first=first, userAuth=True)
        response = GetDropsEntitlementsResponse()
        await self._twitchAPICall(request, response)
        return response
    
    async def UpdateDropsEntitlements(self, entitlement_ids: Optional[List[str]]=None, fulfillment_status: Optional[str]=None) -> UpdateDropsEntitlementsResponse:
        """
        UpdateDropsEntitlements Updates the status of one or more provided drop entitlements to FULFILLED.

        Required Authentication: Requires an app access token or user access token. The client ID in the access token must own the game

        :param entitlement_ids: ID of the broadcaster whose channel is being queried.
        :type entitlement_ids: List[str]
        :param fullfillment_status: ID of the broadcaster whose channel is being queried., defaults to None
        :type fullfillment_status: Optional[str], optional
        :return: data object containing chat settings information
        :rtype: UpdateDropsEntitlementsResponse
        """
        request = UpdateDropsEntitlementsRequest(entitlement_ids=entitlement_ids, fulfillment_status=fulfillment_status)
        response = UpdateDropsEntitlementsResponse()
        await self._twitchAPICall(request, response)
        return response
    
    async def GetExtensionConfigurationSegment(self, extension_id: str, segment:str, broadcaster_id: Optional[str]=None ) -> GetExtensionConfigurationSegmentResponse:
        """
        GetExtensionConfigurationSegment Gets the configuration data for an extension, segmented by a user ID, if provided.

        Required Authentication: Requires a signed JSON Web Token (JWT) created by an Extension Backend Service (EBS). 
                                    For signing requirements, see Signing the JWT. The signed JWT must include the role, 
                                    user_id, and exp fields (see JWT Schema). The role field must be set to external

        :param extension_id: ID of the broadcaster whose channel is being queried.
        :type extension_id: str
        :param segment: ID of the broadcaster whose channel is being queried.
        :type segment: str
        :param broadcaster_id: ID of the broadcaster whose channel is being queried., defaults to None
        :type broadcaster_id: Optional[str], optional
        :return: data object containing chat settings information
        :rtype: GetExtensionConfigurationSegmentResponse
        """
        request = GetExtensionConfigurationSegmentRequest(extension_id=extension_id, segment=segment, broadcaster_id=broadcaster_id)
        response = GetExtensionConfigurationSegmentResponse()
        await self._twitchAPICall(request, response)
        return response
    
    async def SetExtensionConfigurationSegment(self, extension_id: str, segment: str, broadcaster_id: Optional[str]=None, content: Optional[str]=None, version: Optional[str]=None) -> SetExtensionConfigurationSegmentResponse:
        """
        SetExtensionConfigurationSegment Sets the configuration data for an extension, segmented by a user ID, if provided.

        Required Authentication: Requires a signed JSON Web Token (JWT) created by an Extension Backend Service (EBS). 
                                    For signing requirements, see Signing the JWT. The signed JWT must include the role, 
                                    user_id, and exp fields (see JWT Schema). The role field must be set to external

        :param extension_id: ID of the broadcaster whose channel is being queried.
        :type extension_id: str
        :param segment: ID of the broadcaster whose channel is being queried.
        :type segment: str
        :param broadcaster_id: ID of the broadcaster whose channel is being queried., defaults to None
        :type broadcaster_id: Optional[str], optional
        :param content: ID of the broadcaster whose channel is being queried., defaults to None
        :type content: Optional[str], optional
        :param version: ID of the broadcaster whose channel is being queried., defaults to None
        :type version: Optional[str], optional
        :return: data object containing chat settings information
        :rtype: SetExtensionConfigurationSegmentResponse
        """
        request = SetExtensionConfigurationSegmentRequest(extension_id=extension_id, segment=segment, broadcaster_id=broadcaster_id, content=content, version=version)
        response = SetExtensionConfigurationSegmentResponse()
        await self._twitchAPICall(request, response)
        return response
    
    async def SetExtensionRequiredConfiguration(self,broadcaster_id: str, extension_id: str,extension_version:str, required_configuration: str) -> SetExtensionRequiredConfigurationResponse:
        """
        SetExtensionRequiredConfiguration Sets the configuration data for an extension, segmented by a user ID, if provided.

        Required Authentication: Requires a signed JSON Web Token (JWT) created by an Extension Backend Service (EBS). 
                                    For signing requirements, see Signing the JWT. The signed JWT must include the role, 
                                    user_id, and exp fields (see JWT Schema). The role field must be set to external

        :param broadcasters: ID of the broadcaster whose channel is being queried.
        :type broadcasters: str
        :param extension_id: ID of the broadcaster whose channel is being queried.
        :type extension_id: str
        :param extension_version: ID of the broadcaster whose channel is being queried.
        :type extension_version: str
        :param required_configuration: ID of the broadcaster whose channel is being queried.
        :type required_configuration: str
        :return: data object containing chat settings information
        :rtype: SetExtensionRequiredConfigurationResponse
        """
        request = SetExtensionRequiredConfigurationRequest(broadcaster_id=broadcaster_id, extension_id=extension_id, extension_version=extension_version, required_configuration=required_configuration)
        response = SetExtensionRequiredConfigurationResponse()
        await self._twitchAPICall(request, response)
        return response
    
    async def SendExtensionPubSubMessage(self, target: str, content_type: str, message: str, is_global_broadcast: Optional[bool]=False) -> SendExtensionPubSubMessageResponse:
        """
        SendExtensionPubSubMessage Sends a PubSub message to the specified extension.

        Required Authentication: Requires a signed JSON Web Token (JWT) created by an Extension Backend Service (EBS). 
                                    For signing requirements, see Signing the JWT. The signed JWT must include the role, 
                                    user_id, and exp fields (see JWT Schema). The role field must be set to external

        :param target: ID of the broadcaster whose channel is being queried.
        :type target: str
        :param content_type: ID of the broadcaster whose channel is being queried.
        :type content_type: str
        :param message: ID of the broadcaster whose channel is being queried.
        :type message: str
        :return: data object containing chat settings information
        :rtype: SendExtensionPubSubMessageResponse
        """
        request = SendExtensionPubSubMessageRequest(target=target, content_type=content_type, message=message, is_global_broadcast=is_global_broadcast)
        response = SendExtensionPubSubMessageResponse()
        await self._twitchAPICall(request, response)
        return response
    
    async def GetExtensionLiveChannels(self, extension_id: str, first: Optional[str]=None, after: Optional[str]=None, userAuth: bool=False) -> GetExtensionLiveChannelsResponse:
        """
        GetExtensionLiveChannels Gets a list of channels that have installed the specified extension.

        Required Authentication: app access token or user access token

        :param extension_id: ID of the broadcaster whose channel is being queried.
        :type extension_id: str
        :param first: maximum number of objects to return. Maximum: 100. Default: 20., defaults to None
        :type first: Optional[str], optional
        :param after:  The cursor used to fetch the next page of data. This cursor value is received from the response of a previous request., defaults to None
        :type after: Optional[str], optional
        :param userAuth: whether to use user authentication, defaults to False
        :type userAuth: bool, optional
        :return: data object containing chat settings information
        :rtype: GetExtensionLiveChannelsResponse
        """

        request = GetExtensionLiveChannelsRequest(extension_id=extension_id, first=first, after=after,userAuth=userAuth)
        response = GetExtensionLiveChannelsResponse()
        await self._twitchAPICall(request, response)
        return response
    
    async def GetExtensionSecrets(self, extension_id: str) -> GetExtensionSecretsResponse:
        """
        GetExtensionSecrets Gets the secret key for an extension.

        Required Authentication: JWT token with created by an Extension Backend Service (EBS). must include the role, user_id, and exp fields (see JWT Schema). The role field must be set to external

        :param extension_id: ID of the broadcaster whose channel is being queried.
        :type extension_id: str
        :return: data object containing chat settings information
        :rtype: GetExtensionSecretsResponse
        """
        request = GetExtensionSecretsRequest(extension_id=extension_id)
        response = GetExtensionSecretsResponse()
        await self._twitchAPICall(request, response)
        return response
    
    async def CreateExtensionSecret(self, extension_id: str, delay: Optional[int]=None) -> CreateExtensionSecretResponse:
        """
        CreateExtensionSecret Creates a secret for an extension. The created secret value is encrypted before being stored in the database.

        Required Authentication: JWT token with created by an Extension Backend Service (EBS). must include the role, user_id, and exp fields (see JWT Schema). The role field must be set to external

        :param extension_id: ID of the broadcaster whose channel is being queried.
        :type extension_id: str
        :param delay: ID of the broadcaster whose channel is being queried., defaults to None
        :type delay: Optional[int], optional
        :return: data object containing chat settings information
        :rtype: CreateExtensionSecretResponse
        """

        request = CreateExtensionSecretRequest(extension_id=extension_id, delay=delay)
        response = CreateExtensionSecretResponse()
        await self._twitchAPICall(request, response)
        return response
    
    async def SendExtensionChatMessage(self,broadcaster_id: str, text: str, extension_id: str, extension_version: str) -> SendExtensionChatMessageResponse:
        """
        SendExtensionChatMessage Sends a chat message to a specified channel. The extension's name is used as the username for the message in the chat room. To send a chat message, your extension must enable Chat Capabilities (under your extension's Capabilities tab).

        Required Authentication:  JWT token with created by an Extension Backend Service (EBS). must include the role, user_id, and exp fields (see JWT Schema). The role field must be set to external

        :param broadcaster_id: ID of the broadcaster whose channel is being queried.
        :type broadcaster_id: str
        :param text: ID of the broadcaster whose channel is being queried.
        :type text: str
        :param extension_id: ID of the broadcaster whose channel is being queried.
        :type extension_id: str
        :param extension_version: ID of the broadcaster whose channel is being queried.
        :type extension_version: str
        :return: data object containing chat settings information
        :rtype: SendExtensionChatMessageResponse
        """

        request = SendExtensionChatMessageRequest(broadcaster_id=broadcaster_id, text=text, extension_id=extension_id, extension_version=extension_version)
        response = SendExtensionChatMessageResponse()
        await self._twitchAPICall(request, response)
        return response
    
    async def GetExtensions(self, extension_id: str, extension_version: Optional[str]=None) -> GetExtensionsResponse:
        """
        GetExtensions Gets information about specified extensions.

        Required Authentication: JWT token with created by an Extension Backend Service (EBS). must include the role, role must be set to external
        :param extension_id: ID of the broadcaster whose channel is being queried.
        :type extension_id: str
        :param extension_version: The version of the extension to get. If not specified, it returns the latest version., defaults to None
        :type extension_version: Optional[str], optional
        :return: data object containing chat settings information
        :rtype: GetExtensionsResponse
        """

        request = GetExtensionsRequest(extension_id=extension_id, extension_version=extension_version)
        response = GetExtensionsResponse()
        await self._twitchAPICall(request, response)
        return response

    async def GetReleasedExtensions(self, extension_id: str, extension_version: Optional[str]=None) -> GetReleasedExtensionsResponse:
        """
        GetReleasedExtensions Gets information about specified extensions.

        Required Authentication: app access token or user access token

        :param extension_id: ID of the broadcaster whose channel is being queried.
        :type extension_id: str
        :param extension_version: The version of the extension to get. If not specified, it returns the latest version., defaults to None
        :type extension_version: Optional[str], optional
        :return: data object containing chat settings information   
        :rtype: GetReleasedExtensionsResponse
        """
        request = GetReleasedExtensionsRequest(extension_id=extension_id, extension_version=extension_version)
        response = GetReleasedExtensionsResponse()
        await self._twitchAPICall(request, response)
        return response

    async def GetExtensionBitsProducts(self) -> GetExtensionBitsProductsResponse:
        request = GetExtensionBitsProductsRequest()
        response = GetExtensionBitsProductsResponse()
        await self._twitchAPICall(request, response)
        return response
    
    async def UpdateExtensionBitsProduct(self) -> UpdateExtensionBitsProductResponse:
        request = UpdateExtensionBitsProductRequest()
        response = UpdateExtensionBitsProductResponse()
        await self._twitchAPICall(request, response)
        return response
    
    async def CreateEventSubSubscription(self) -> CreateEventSubSubscriptionResponse:
        request = CreateEventSubSubscriptionRequest()
        response = CreateEventSubSubscriptionResponse()
        await self._twitchAPICall(request, response)
        return response
    
    async def DeleteEventSubSubscription(self) -> DeleteEventSubSubscriptionResponse:
        request = DeleteEventSubSubscriptionRequest()
        response = DeleteEventSubSubscriptionResponse()
        await self._twitchAPICall(request, response)
        return response
    
    async def GetEventSubSubscriptions(self) -> GetEventSubSubscriptionsResponse:
        request = GetEventSubSubscriptionsRequest()
        response = GetEventSubSubscriptionsResponse()
        await self._twitchAPICall(request, response)
        return response

    async def GetTopGames(self) -> GetTopGamesResponse:
        request = GetTopGamesRequest()
        response = GetTopGamesResponse()
        await self._twitchAPICall(request, response)
        return response
    
    async def GetGames(self) -> GetGamesResponse:
        request = GetGamesRequest()
        response = GetGamesResponse()
        await self._twitchAPICall(request, response)
        return response
    
    async def GetCreatorGoals(self) -> GetCreatorGoalsResponse:
        request = GetCreatorGoalsRequest()
        response = GetCreatorGoalsResponse()
        await self._twitchAPICall(request, response)
        return response
    
    async def GetHypeTrainEvents(self) -> GetHypeTrainEventsResponse:
        request = GetHypeTrainEventsRequest()
        response = GetHypeTrainEventsResponse()
        await self._twitchAPICall(request, response)
        return response
    
    async def CheckAutoModStatus(self) -> CheckAutoModStatusResponse:
        request = CheckAutoModStatusRequest()
        response = CheckAutoModStatusResponse()
        await self._twitchAPICall(request, response)
        return response
    
    async def ManageHeldAutoModMessages(self) -> ManageHeldAutoModMessagesResponse:
        request = ManageHeldAutoModMessagesRequest()
        response = ManageHeldAutoModMessagesResponse()
        await self._twitchAPICall(request, response)
        return response
    
    async def GetAutoModSettings(self) -> GetAutoModSettingsResponse:
        request = GetAutoModSettingsRequest()
        response = GetAutoModSettingsResponse()
        await self._twitchAPICall(request, response)
        return response
    
    async def UpdateAutoModSettings(self) -> UpdateAutoModSettingsResponse:
        request = UpdateAutoModSettingsRequest()
        response = UpdateAutoModSettingsResponse()
        await self._twitchAPICall(request, response)
        return response
    
    async def GetBannedUsers(self) -> GetBannedUsersResponse:
        request = GetBannedUsersRequest()
        response = GetBannedUsersResponse()
        await self._twitchAPICall(request, response)
        return response
    
    async def BanUser(self) -> BanUserResponse:
        request = BanUserRequest()
        response = BanUserResponse()
        await self._twitchAPICall(request, response)
        return response
    
    async def UnbanUser(self) -> UnbanUserResponse:
        request = UnbanUserRequest()
        response = UnbanUserResponse()
        await self._twitchAPICall(request, response)
        return response
    
    async def GetBlockedTerms(self) -> GetBlockedTermsResponse:
        request = GetBlockedTermsRequest()
        response = GetBlockedTermsResponse()
        await self._twitchAPICall(request, response)
        return response
    
    async def AddBlockedTerm(self) -> AddBlockedTermResponse:
        request = AddBlockedTermRequest()
        response = AddBlockedTermResponse()
        await self._twitchAPICall(request, response)
        return response
    
    async def RemoveBlockedTerm(self) -> RemoveBlockedTermResponse:
        request = RemoveBlockedTermRequest()
        response = RemoveBlockedTermResponse()
        await self._twitchAPICall(request, response)
        return response

    async def DeleteChatMessages(self) -> DeleteChatMessagesResponse:
        request = DeleteChatMessagesRequest()
        response = DeleteChatMessagesResponse()
        await self._twitchAPICall(request, response)
        return response
    
    async def GetModerators(self) -> GetModeratorsResponse:
        request = GetModeratorsRequest()
        response = GetModeratorsResponse()
        await self._twitchAPICall(request, response)
        return response
    
    async def AddChannelModerator(self) -> AddChannelModeratorResponse:
        request = AddChannelModeratorRequest()
        response = AddChannelModeratorResponse()
        await self._twitchAPICall(request, response)
        return response
    
    async def RemoveChannelModerator(self) -> RemoveChannelModeratorResponse:
        request = RemoveChannelModeratorRequest()
        response = RemoveChannelModeratorResponse()
        await self._twitchAPICall(request, response)
        return response
    
    async def GetVIPs(self) -> GetVIPsResponse:
        request = GetVIPsRequest()
        response = GetVIPsResponse()
        await self._twitchAPICall(request, response)
        return response
    
    async def AddChannelVIP(self) -> AddChannelVIPResponse:
        request = AddChannelVIPRequest()
        response = AddChannelVIPResponse()
        await self._twitchAPICall(request, response)
        return response
    
    async def RemoveChannelVIP(self) -> RemoveChannelVIPResponse:
        request = RemoveChannelVIPRequest()
        response = RemoveChannelVIPResponse()
        await self._twitchAPICall(request, response)
        return response
    
    async def UpdateShieldModeStatus(self) -> UpdateShieldModeStatusResponse:
        request = UpdateShieldModeStatusRequest()
        response = UpdateShieldModeStatusResponse()
        await self._twitchAPICall(request, response)
        return response
    
    async def GetShieldModeStatus(self) -> GetShieldModeStatusResponse:
        request = GetShieldModeStatusRequest()
        response = GetShieldModeStatusResponse()
        await self._twitchAPICall(request, response)
        return response
    
    async def GetPolls(self) -> GetPollsResponse:
        request = GetPollsRequest()
        response = GetPollsResponse()
        await self._twitchAPICall(request, response)
        return response
    
    async def CreatePoll(self) -> CreatePollResponse:
        request = CreatePollRequest()
        response = CreatePollResponse()
        await self._twitchAPICall(request, response)
        return response
    
    async def EndPoll(self) -> EndPollResponse:
        request = EndPollRequest()
        response = EndPollResponse()
        await self._twitchAPICall(request, response)
        return response
    
    async def GetPredictions(self) -> GetPredictionsResponse:
        request = GetPredictionsRequest()
        response = GetPredictionsResponse()
        await self._twitchAPICall(request, response)
        return response
    
    async def CreatePrediction(self) -> CreatePredictionResponse:
        request = CreatePredictionRequest()
        response = CreatePredictionResponse()
        await self._twitchAPICall(request, response)
        return response
    
    async def EndPrediction(self) -> EndPredictionResponse:
        request = EndPredictionRequest()
        response = EndPredictionResponse()
        await self._twitchAPICall(request, response)
        return response
    
    async def Startaraid(self) -> StartaraidResponse:
        request = StartaraidRequest()
        response = StartaraidResponse()
        await self._twitchAPICall(request, response)
        return response
    
    async def Cancelaraid(self) -> CancelaraidResponse:
        request = CancelaraidRequest()
        response = CancelaraidResponse()
        await self._twitchAPICall(request, response)
        return response
    
    async def GetChannelStreamSchedule(self) -> GetChannelStreamScheduleResponse:
        request = GetChannelStreamScheduleRequest()
        response = GetChannelStreamScheduleResponse()
        await self._twitchAPICall(request, response)
        return response
    
    async def GetChanneliCalendar(self) -> GetChanneliCalendarResponse:
        request = GetChanneliCalendarRequest()
        response = GetChanneliCalendarResponse()
        await self._twitchAPICall(request, response)
        return response
    
    async def UpdateChannelStreamSchedule(self) -> UpdateChannelStreamScheduleResponse:
        request = UpdateChannelStreamScheduleRequest()
        response = UpdateChannelStreamScheduleResponse()
        await self._twitchAPICall(request, response)
        return response
    
    async def CreateChannelStreamScheduleSegment(self, broadcaster_id: str, start_time: Optional[str]=None, duration: Optional[str]=None, category_id: Optional[str]=None, title: Optional[str]=None, is_canceled: Optional[bool]=None, timezone: Optional[str]=None) -> CreateChannelStreamScheduleSegmentResponse:
        """
        CreateChannelStreamScheduleSegment Creates a specified channel stream schedule segment.

        Required Authentication: User access token with channel:manage:schedule scope.

        :param broadcaster_id: ID of the broadcaster whose channel is being queried.
        :type broadcaster_id: str
        :param start_time: ID of the broadcaster whose channel is being queried., defaults to None
        :type start_time: Optional[str], optional
        :param duration: ID of the broadcaster whose channel is being queried., defaults to None
        :type duration: Optional[str], optional
        :param category_id: ID of the broadcaster whose channel is being queried., defaults to None
        :type category_id: Optional[str], optional
        :param title: ID of the broadcaster whose channel is being queried., defaults to None
        :type title: Optional[str], optional
        :param is_canceled: ID of the broadcaster whose channel is being queried., defaults to None
        :type is_canceled: Optional[bool], optional
        :param timezone: ID of the broadcaster whose channel is being queried., defaults to None
        :type timezone: Optional[str], optional
        :return: data object containing chat settings information
        :rtype: CreateChannelStreamScheduleSegmentResponse
        """
        
        request = CreateChannelStreamScheduleSegmentRequest()
        response = CreateChannelStreamScheduleSegmentResponse()
        await self._twitchAPICall(request, response)
        return response
    
    async def UpdateChannelStreamScheduleSegment(self,broadcaster_id: str, id: str, start_time: Optional[str]=None, duration: Optional[str]=None, category_id: Optional[str]=None, title: Optional[str]=None, is_canceled: Optional[bool]=None, timezone: Optional[str]=None) -> UpdateChannelStreamScheduleSegmentResponse:
        """
        UpdateChannelStreamScheduleSegment Updates a specified channel stream schedule segment.

        Required Authentication: User access token with channel:manage:schedule scope.

        :param broadcaster_id: ID of the broadcaster whose channel is being queried.
        :type broadcaster_id: str
        :param id: ID of the broadcast segment to update.
        :type id: str
        :return: data object containing chat settings information
        :rtype: UpdateChannelStreamScheduleSegmentResponse
        """

        request = UpdateChannelStreamScheduleSegmentRequest()
        response = UpdateChannelStreamScheduleSegmentResponse()
        await self._twitchAPICall(request, response)
        return response
    
    async def DeleteChannelStreamScheduleSegment(self,broadcaster_id: str, id: str) -> DeleteChannelStreamScheduleSegmentResponse:
        """
        DeleteChannelStreamScheduleSegment Deletes a specified channel stream schedule segment.

        Required Authentication: User access token with channel:manage:schedule scope.

        :param broadcaster_id: ID of the broadcaster whose channel is being queried.
        :type broadcaster_id: str
        :param id: ID of the broadcast segment to remove from the schedule. 
        :type id: str
        :return: data object containing chat settings information
        :rtype: DeleteChannelStreamScheduleSegmentResponse
        """
        request = DeleteChannelStreamScheduleSegmentRequest(broadcaster_id=broadcaster_id, id=id)
        response = DeleteChannelStreamScheduleSegmentResponse()
        await self._twitchAPICall(request, response)
        return response
    
    async def SearchCategories(self, query: str, first: Optional[int]=None, after: Optional[str]=None, userAuth: Optional[bool]=False) -> SearchCategoriesResponse:
        """
        SearchCategories Gets the game or category channels that match the search query.

        Required Authentication: app access token or user access token

        :param query: ID of the broadcaster whose channel is being queried.
        :type query: str
        :param first: maximum number of objects to return. Maximum: 100. Default: 20., defaults to None
        :type first: Optional[int], optional
        :param after:  The cursor used to fetch the next page of data. This cursor value is received from the response of a previous request., defaults to None
        :type after: Optional[str], optional
        :param userAuth: whether to use user authentication, defaults to False
        :type userAuth: Optional[bool], optional
        :return: data object containing chat settings information
        :rtype: SearchCategoriesResponse
        """
        request = SearchCategoriesRequest(query=query, first=first, after=after, userAuth=userAuth)
        response = SearchCategoriesResponse()
        await self._twitchAPICall(request, response)
        return response
    
    async def SearchChannels(self, query: str, live_only: Optional[bool]=False, first: Optional[int]=None, after: Optional[str]=None, userAuth: Optional[bool]=False) -> SearchChannelsResponse:
        """
        SearchChannels Gets information about specified streams.

        Required Authentication: app access token or user access token

        :param query: ID of the broadcaster whose channel is being queried.
        :type query: str
        :param live_only: determines whether to search only for live streams or both live and offline streams, defaults to False
        :type live_only: Optional[bool], optional
        :param first: maximum number of objects to return. Maximum: 100. Default: 20., defaults to None
        :type first: Optional[int], optional
        :param after:  The cursor used to fetch the next page of data. This cursor value is received from the response of a previous request., defaults to None
        :type after: Optional[str], optional
        :param userAuth: whether to use user authentication, defaults to False
        :type userAuth: Optional[bool], optional
        :return: data object containing chat settings information
        :rtype: SearchChannelsResponse
        """
        request = SearchChannelsRequest(query=query, first=first, after=after, live_only=live_only, userAuth=userAuth)
        response = SearchChannelsResponse()
        await self._twitchAPICall(request, response)
        return response
    
    async def GetStreamKey(self) -> GetStreamKeyResponse:
        """
        GetStreamKey Gets stream key for the authenticated user.

        Required Authentication: user access token that has the channel:read:stream_key scope

        :return: data object containing chat settings information
        :rtype: GetStreamKeyResponse
        """

        request = GetStreamKeyRequest(broadcaster_id=self._user.id)
        response = GetStreamKeyResponse()
        await self._twitchAPICall(request, response)
        return response
    
    async def GetUserStreams(self, game_id: Optional[str]=None, type: Optional[str]=None, language: Optional[str]=None, before: Optional[str]=None, after: Optional[str]=None, first: Optional[str]=None) -> GetStreamsResponse:
        """
        GetUserStreams Gets information about specified streams.

        Required Authentication: user access token

        :param game_id: ID of the broadcaster whose channel is being queried., defaults to None
        :type game_id: Optional[str], optional
        :param type: ID of the broadcaster whose channel is being queried., defaults to None
        :type type: Optional[str], optional
        :param language: ID of the broadcaster whose channel is being queried., defaults to None
        :type language: Optional[str], optional
        :param before: ID of the broadcaster whose channel is being queried., defaults to None
        :type before: Optional[str], optional
        :param after: ID of the broadcaster whose channel is being queried., defaults to None
        :type after: Optional[str], optional
        :param first: ID of the broadcaster whose channel is being queried., defaults to None
        :type first: Optional[str], optional
        :return: data object containing chat settings information
        :rtype: GetStreamsResponse
        """
        request = GetStreamsRequest(user_id=self._user.id, game_id=game_id, type=type, language=language, before=before, after=after, first=first, userAuth=True)
        response = GetStreamsResponse()
        await self._twitchAPICall(request, response)
        return response    
    
    async def GetStreams(self, user_id: Optional[str] = None, user_login: Optional[str] = None, 
                     game_id: Optional[str] = None, type: Optional[str] = None, 
                     language: Optional[str] = None, before: Optional[str] = None, 
                     after: Optional[str] = None, first: Optional[str] = None, userAuth=False) -> GetStreamsResponse:
        """
        GetStreams Gets information about specified streams.

        Required Authentication: app access token or user access token

        :param user_id: ID of the broadcaster whose channel is being queried., defaults to None
        :type user_id: Optional[str], optional
        :param user_login: ID of the broadcaster whose channel is being queried., defaults to None
        :type user_login: Optional[str], optional
        :param game_id: ID of the broadcaster whose channel is being queried., defaults to None
        :type game_id: Optional[str], optional
        :param type: ID of the broadcaster whose channel is being queried., defaults to None
        :type type: Optional[str], optional
        :param language: ID of the broadcaster whose channel is being queried., defaults to None
        :type language: Optional[str], optional
        :param before: ID of the broadcaster whose channel is being queried., defaults to None
        :type before: Optional[str], optional
        :param after: ID of the broadcaster whose channel is being queried., defaults to None
        :type after: Optional[str], optional
        :param first: ID of the broadcaster whose channel is being queried., defaults to None
        :type first: Optional[str], optional
        :return: data object containing chat settings information
        :rtype: GetStreamsResponse
        """

        request = GetStreamsRequest(user_id=user_id, user_login=user_login, game_id=game_id, type=type, language=language, before=before, after=after, first=first, userAuth=userAuth)
        response = GetStreamsResponse()
        await self._twitchAPICall(request, response)
        return response
    
    async def GetFollowedStreams(self, user_id: str, first: Optional[int]=None, after: Optional[str]=None) -> GetFollowedStreamsResponse:
        """
        GetFollowedStreams Gets information about followed streams.

        Required Authentication: app access token or user access token

        :param user_id: ID of the broadcaster whose channel is being queried.
        :type user_id: str
        :param first: maximum number of objects to return. Maximum: 100. Default: 20., defaults to None
        :type first: Optional[int], optional
        :param after:  The cursor used to fetch the next page of data. This cursor value is received from the response of a previous request., defaults to None
        :type after: Optional[str], optional
        :return: data object containing chat settings information
        :rtype: GetFollowedStreamsResponse
        """

        request = GetFollowedStreamsRequest()
        response = GetFollowedStreamsResponse()
        await self._twitchAPICall(request, response)
        return response
    
    async def CreateStreamMarker(self, user_id: str, description: Optional[str]=None) -> CreateStreamMarkerResponse:
        request = CreateStreamMarkerRequest(user_id=user_id, description=description)
        response = CreateStreamMarkerResponse()
        await self._twitchAPICall(request, response)
        return response
    
    async def GetStreamMarkers(self, user_id: str, video: Optional[str]=None, first: Optional[str]=None, before: Optional[str]=None, after: Optional[str]=None ) -> GetStreamMarkersResponse:
        """
        GetStreamMarkers Gets information about specified extensions.

        Required Authentication: app access token or user access token

        :param user_id: ID of the broadcaster whose channel is being queried.
        :type user_id: str
        :param video: ID of the broadcaster whose channel is being queried., defaults to None
        :type video: Optional[str], optional
        :param first: maximum number of objects to return. Maximum: 100. Default: 20., defaults to None
        :type first: Optional[str], optional
        :param after:  The cursor used to fetch the next page of data. This cursor value is received from the response of a previous request., defaults to None
        :type after: Optional[str], optional
        :param before:  The cursor used to fetch the previous page of data. This cursor value is received from the response of a previous request., defaults to None
        :type before: Optional[str], optional
        :return: data object containing chat settings information
        :rtype: GetStreamMarkersResponse
        """
        request = GetStreamMarkersRequest(user_id=user_id, video=video, first=first, before=before, after=after)
        response = GetStreamMarkersResponse()
        await self._twitchAPICall(request, response)
        return response
    
    async def GetBroadcasterSubscriptions(self, broadcaster_id: str, user_id: Optional[str]=None, first : Optional[str]=None, after: Optional[str]=None, before: Optional[str]=None) -> GetBroadcasterSubscriptionsResponse:
        """
        GetBroadcasterSubscriptions Gets information about all of a broadcaster’s subscriptions.

        Required Authentication: app access token or user access token

        :param broadcaster_id: ID of the broadcaster whose channel is being queried.
        :type broadcaster_id: str
        :param user_id: ID of the broadcaster whose channel is being queried., defaults to None
        :type user_id: Optional[str], optional
        :param first: maximum number of objects to return. Maximum: 100. Default: 20., defaults to None
        :type first: Optional[str], optional
        :param after:  The cursor used to fetch the next page of data. This cursor value is received from the response of a previous request., defaults to None
        :type after: Optional[str], optional
        :param before:  The cursor used to fetch the previous page of data. This cursor value is received from the response of a previous request., defaults to None
        :type before: Optional[str], optional
        :return: data object containing chat settings information
        :rtype: GetBroadcasterSubscriptionsResponse
        """
        request = GetBroadcasterSubscriptionsRequest(broadcaster_id=broadcaster_id, user_id=user_id, first=first, after=after, before=before)
        response = GetBroadcasterSubscriptionsResponse()
        await self._twitchAPICall(request, response)
        return response
    
    async def CheckUserSubscription(self, broadcaster_id: str, user_id: str) -> CheckUserSubscriptionResponse:
        """
        CheckUserSubscription Checks if a specified user is subscribed to a specified channel. Intended for use by channel owners.

        Required Authentication: app access token or user access token

        :param broadcaster_id: ID of the broadcaster whose channel is being queried.
        :type broadcaster_id: str
        :param user_id: ID of the broadcaster whose channel is being queried.
        :type user_id: str
        :return: data object containing chat settings information
        :rtype: CheckUserSubscriptionResponse
        """
        request = CheckUserSubscriptionRequest(broadcaster_id=broadcaster_id, user_id=user_id)
        response = CheckUserSubscriptionResponse()
        await self._twitchAPICall(request, response)
        return response

    async def GetChannelTeams(self, broadcaster_id: str, userAuth=False) -> GetChannelTeamsResponse:
        """
        GetChannelTeams Gets information about the teams to which a specified channel belongs.

        Required Authentication: app access token or user access token

        :param broadcaster_id: ID of the broadcaster whose channel is being queried.
        :type broadcaster_id: str
        :return: data object containing chat settings information
        :rtype: GetChannelTeamsResponse
        """

        request = GetChannelTeamsRequest(broadcaster_id=broadcaster_id, userAuth=userAuth)
        response = GetChannelTeamsResponse()
        await self._twitchAPICall(request, response)
        return response

    async def GetTeams(self, name: Optional[str]= None, id: Optional[str]=None) -> GetTeamsResponse:
        """
        GetTeams Gets information about specified teams. name or id must be specified, but not both.

        Required Authentication: app access token or user access token

        raises: ValueError if both name and id are not specified
        raises: ValueError if both name and id are specified

        :param name: ID of the broadcaster whose channel is being queried., defaults to None
        :type name: Optional[str], optional
        :param id: ID of the broadcaster whose channel is being queried., defaults to None
        :type id: Optional[str], optional
        :return: data object containing chat settings information
        :rtype: GetTeamsResponse
        """

        request = GetTeamsRequest(name=name, id=id)
        response = GetTeamsResponse()
        await self._twitchAPICall(request, response)
        return response
    
    async def GetUsers(self,id:Optional[str]=None, login: Optional[str]=None) -> GetUsersResponse:
        """
        GetUsers Gets information about one or more specified Twitch users. Users are identified by optional user IDs and/or login name. If neither a user ID nor a login name is specified, the user is looked up by Bearer token.

        Required Authentication: app access token or user access token

        :param id: ID of the broadcaster whose channel is being queried., defaults to None
        :type id: Optional[str], optional
        :param login: ID of the broadcaster whose channel is being queried., defaults to None
        :type login: Optional[str], optional
        :return: data object containing chat settings information
        :rtype: GetUsersResponse
        """
        request = GetUsersRequest(id=id, login=login)
        response = GetUsersResponse()
        await self._twitchAPICall(request, response)
        return response
    
    async def UpdateUser(self, discription: Optional[str]="") -> UpdateUserResponse:
        """
        UpdateUser Updates the description of a user specified by a Bearer token.

        Required Authentication: Requires a user access token with the user:edit scope.

        :param discription: description of the user, defaults to ""
        :type discription: Optional[str], optional
        :return: data object with response code
        :rtype: UpdateUserResponse
        """
        request = UpdateUserRequest(description=discription)
        response = UpdateUserResponse()
        await self._twitchAPICall(request, response)
        return response

    async def GetUserBlockList(self, broadcaster_id: str, first: Optional[int]=None, after: Optional[str]=None) -> GetUserBlockListResponse:
        """
        GetUserBlockList Gets information about a specified user’s block list.

        Required Authentication: user access token with the user:read:blocked_users scope.

        :param broadcaster_id: ID of the broadcaster whose channel is being queried.
        :type broadcaster_id: str
        :param first: maximum number of objects to return. Maximum: 100. Default: 20., defaults to None
        :type first: Optional[int], optional
        :param after:  The cursor used to fetch the next page of data. This cursor value is received from the response of a previous request., defaults to None
        :type after: Optional[str], optional
        :return: data object with wit a list of videos
        :rtype: GetUserBlockListResponse
        """
        request = GetUserBlockListRequest(broadcaster_id=broadcaster_id, first=first, after=after)
        response = GetUserBlockListResponse()
        await self._twitchAPICall(request, response)
        return response
    
    async def BlockUser(self, target_user_id: str, source_context: Optional[str]=None, reason: Optional[str]=None) -> BlockUserResponse:
        """
        BlockUser Blocks a user; that is, adds a specified target user to the blocks list of the authenticated user.

        Required Authentication: user access token with the user:manage:blocked_users scope.

        :param target_user_id: ID of the broadcaster to be blocked.
        :type target_user_id: str
        :param source_context: where harrasment is coming from (chat, whisper), defaults to None
        :type source_context: Optional[str], optional
        :param reason: reason for blocking, defaults to None
        :type reason: Optional[str], optional
        :return: data object with response code
        :rtype: BlockUserResponse
        """
        request = BlockUserRequest(target_user_id=target_user_id, source_context=source_context, reason=reason)
        response = BlockUserResponse()
        await self._twitchAPICall(request, response)
        return response
    
    async def UnblockUser(self, target_user_id: str) -> UnblockUserResponse:
        """
        UnblockUser Unblocks a user; that is, deletes a user from the blocks list of the authenticated user.

        Required Authentication: user access token with the user:manage:blocked_users scope.

        :param target_user_id: ID of the broadcaster whose channel is being queried.
        :type target_user_id: str
        :return: data object with response code
        :rtype: UnblockUserResponse
        """

        request = UnblockUserRequest(target_user_id=target_user_id)
        response = UnblockUserResponse()
        await self._twitchAPICall(request, response)
        return response
    
    async def GetUserExtensions(self) -> GetUserExtensionsResponse:
        """
        GetUserExtensions Gets information about active extensions installed by a user.

        Required Authentication: user access token with the user:read:broadcast or user:edit:broadcast scope.
        
        :return: data object with wit a list of videos
        :rtype: GetUserExtensionsResponse
        """
        
        request = GetUserExtensionsRequest()
        response = GetUserExtensionsResponse()
        await self._twitchAPICall(request, response)
        return response

    async def GetUserActiveExtensions(self, user_id: Optional[str], userAuth:Optional[bool]=False) -> GetUserActiveExtensionsResponse:
        """
        GetUserActiveExtensions Gets information about active extensions installed by a specified user, identified by a user ID or login name.

        Required Authentication: app access token or user access token with the user:read:broadcast or user:edit:broadcast scope.

        :return: data object with wit a list of videos
        :rtype: GetUserActiveExtensionsResponse
        """
        request = GetUserActiveExtensionsRequest(user_id=user_id, userAuth=userAuth)
        response = GetUserActiveExtensionsResponse()
        await self._twitchAPICall(request, response)
        return response
    
    
    async def GetUserActiveExtensions(self, user_id:str) -> GetUserActiveExtensionsResponse:
        """
        GetUserActiveExtensions Gets information about active extensions installed by a specified user, identified by a user ID or login name.

        Required Authentication: app access token or user access token with the user:read:broadcast or user:edit:broadcast scope.

        :return: data object with wit a list of videos
        :rtype: GetUserActiveExtensionsResponse
        """
        request = GetUserActiveExtensionsRequest(user_id=user_id)
        response = GetUserActiveExtensionsResponse()
        await self._twitchAPICall(request, response)
        return response
   
    async def UpdateUserExtensions(self, panel: Optional[dict[str, ExtensionItem]]=None, overlay: Optional[dict[str, ExtensionItem]]=None, component:  Optional[dict[str, ExtensionItem]]=None,) -> UpdateUserExtensionsResponse:
        """
        UpdateUserExtensions Updates the activation state, extension ID, and/or version number of installed extensions for a specified user.

        Required Authentication: user access token with user:edit:broadcast scope.

        :param panel: ID of the broadcaster whose channel is being queried.
        :type panel: dict[str, ExtensionItem]
        :param overlay: ID of the broadcaster whose channel is being queried.
        :type overlay: dict[str, ExtensionItem]
        :param component: ID of the broadcaster whose channel is being queried.
        :type component: dict[str, ExtensionItem]
        :return: data object with wit a list of videos
        :rtype: UpdateUserExtensionsResponse
        """

        request = UpdateUserExtensionsRequest(panel=panel, overlay=overlay, component=component)
        response = UpdateUserExtensionsResponse()
        await self._twitchAPICall(request, response)
        return response

    async def GetVideos(self, id: Optional[list[str]]=None, user_id: Optional[str]=None, 
            game_id: Optional[str]=None, language: Optional[str]=None, 
            period: Optional[str]=None, sort: Optional[str]=None, 
            type: Optional[str]=None, first: Optional[str]=None, 
            after: Optional[str]=None, before: Optional[str]=None) -> GetVideosResponse:
        """
        GetVideos Gets video information by video ID (one or more), user ID (one only), or game ID (one only).

        Required Authentication: App access token or user access token.

        :param id: ID of the broadcaster whose channel is being queried.
        :type id: str
        :param user_id: ID of the broadcaster whose channel is being queried.
        :type user_id: str
        :param game_id: ID of the broadcaster whose channel is being queried.
        :type game_id: str
        :param language: ID of the broadcaster whose channel is being queried.
        :type language: str
        :param period: ID of the broadcaster whose channel is being queried.
        :type period: str
        :param sort: ID of the broadcaster whose channel is being queried.
        :type sort: str
        :param type: ID of the broadcaster whose channel is being queried.
        :type type: str
        :param first: ID of the broadcaster whose channel is being queried.
        :type first: str
        :param after: ID of the broadcaster whose channel is being queried.
        :type after: str
        :param before: ID of the broadcaster whose channel is being queried.
        :type before: str
        :return: data object with wit a list of videos
        :rtype: GetVideosResponse
        """

        request = GetVideosRequest(id=id, user_id=user_id, game_id=game_id, language=language, period=period, sort=sort, type=type, first=first, after=after, before=before)
        response = GetVideosResponse()
        await self._twitchAPICall(request, response)
        return response

    async def DeleteVideos(self, id: str | list ) -> DeleteVideosResponse:
        """
        DeleteVideos Deletes videos specified by video ID (one or more), user ID (one only), or game ID (one only).

        Required Authentication: user access token with the channel:manage:videos scope.

        :param id: ID of the broadcaster whose channel is being queried.
        :type id: str | list
        :return: data object with wit a list of deleted video ids
        :rtype: DeleteVideosResponse
        """
        request = DeleteVideosRequest(id)
        response = DeleteVideosResponse()
        await self._twitchAPICall(request, response)
        return response
       

    async def SendWhisper(self, to_user_id: str, message: str) -> SendWhisperResponse:
        """
        SendWhisper Sends a whisper message to a specified user from the currently authenticated user.

        Required Authentication: Requires a valid OAuth token.

        :param to_user_id: ID of the broadcaster whose channel is being queried.
        :type to_user_id: str
        :param message: ID of the broadcaster whose channel is being queried.
        :type message: str
        :return: data object with status code
        :rtype: SendWhisperResponse
        """
        request = SendWhisperRequest(self._credentials[SendWhisperRequest.authorization].id, to_user_id, message)
        response = SendWhisperResponse()
        await self._twitchAPICall(request, response)
        return response