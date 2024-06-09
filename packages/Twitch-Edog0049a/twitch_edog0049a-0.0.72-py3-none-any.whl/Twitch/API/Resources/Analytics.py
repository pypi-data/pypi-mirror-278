from Twitch.API.Resources.__imports import *
"""
Get Extension Analytics
"""

class GetExtensionAnalyticsRequest(Utils.RequestBaseClass):
    """
    GetExtensionAnalyticsRequest:
     
    Gets an analytics report for one or more extensions. The response contains the URLs used to download the reports (CSV files). Learn More
        Authorization
            Requires a user access token that includes the analytics:read:extensions scope.

        :param extension_id:  The extension’s client ID. If specified, the response contains a report 
            for the specified extension. If not specified, the response includes a report for each extension that the 
            authenticated user owns.
        :type extension_id: str, optional
        
        :param type: _description_, defaults to None
        :type type: Optional[str], optional
        :param started_at: _description_, defaults to None
        :type started_at: Optional[datetime], optional
        :param ended_at: _description_, defaults to None
        :type ended_at: Optional[datetime], optional
        :param first: _description_, defaults to None
        :type first: Optional[int], optional
        :param after: _description_, defaults to None
        :type after: Optional[str], optional
    """    
    requestType = Utils.HTTPMethod.GET
    scope = Scope.Analytics.Read.Extensions
    authorization = Utils.AuthRequired.USER
    endPoint = "/analytics/extensions"


    def __init__(self, 
                extension_id: Optional[str]=None, 
                type: Optional[str]=None,
                started_at: Optional[datetime]=None,
                ended_at: Optional[datetime]=None,
                first: Optional[int]=None,
                after: Optional[str]=None
                    ) -> None:
        """
        __init__ _summary_

        _extended_summary_

        """      
        self.extension_id = extension_id
        self.type = type
        self.started_at = started_at.isoformat("T") if isinstance(started_at, datetime) else started_at
        self.ended_at = ended_at.isoformat("T") if isinstance(ended_at, datetime) else started_at
        self.first = first
        self.after = after 
        super().__init__()

class ExtensionAnalyticsItem(Utils.DateRangeMixin):  
    extension_id:str
    URL:str
    type:str

class GetExtensionAnalyticsResponse(Utils.PagenationMixin, Utils.ResponseBaseClass):
    def __init__(self) -> None:
        super().__init__(ExtensionAnalyticsItem)

"""
Get Game Analytics
"""   
class GetGameAnalyticsRequest(Utils.RequestBaseClass):
    """
    Gets an analytics report for one or more extensions. The response contains the URLs used to download the reports (CSV files)
        Authorization
            Requires a user access token that includes the analytics:read:extensions scope.

    :class: GetGameAnalyticsRequest 

    :param game_id:	The extension’s client ID. If specified, the response contains a report for the specified extension. If not specified, the response includes a report for each extension that the authenticated user owns.
    

                                            
        
    """

    requestType = Utils.HTTPMethod.GET
    scope = Scope.Analytics.Read.Extensions
    authorization = Utils.AuthRequired.USER
    endPoint = "/analytics/extensions"
    game_id: str
    date_range: Utils.dateRange

    def __init__(self, 
                 game_id: Optional[str] = None,
                 type: Optional[str]= None,
                 started_at: Optional[datetime] = None,
                 ended_at: Optional[datetime] = None,
                 first: Optional[int] = None,
                 after: Optional[str] = None
                    ) -> None:
        
        self.game_id = game_id
        self.type = type
        self.started_at = started_at.isoformat("T") if isinstance(started_at, datetime) else started_at
        self.ended_at = ended_at.isoformat("T") if isinstance(ended_at, datetime) else started_at
        self.first = first
        self.after = after 
        super().__init__()

class GameAnalyticsItem(Utils.DateRangeMixin):
    def __init__(self) -> None:
        self.game_id:str
        self.URL:str
        self.type:str
        
class GetGameAnalyticsResponse(Utils.PagenationMixin, Utils.ResponseBaseClass):
    def __init__(self) -> None:
        super().__init__(GameAnalyticsItem)