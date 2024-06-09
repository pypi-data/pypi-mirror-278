from Twitch.API.Resources.__imports import *

class GetChannelStreamScheduleRequest(Utils.RequestBaseClass):
    requestType = Utils.HTTPMethod.GET
    scope = None
    authorization = Utils.AuthRequired.CLIENT
    endPoint ="/schedule"
    def __init__(self, broadcaster_id: str, id: Optional[str]=None, start_time: Optional[str]=None, utc_offset: Optional[str]=None, first: Optional[str]=None, after: Optional[str]=None, userAuth=False) -> None:
        if userAuth:
            self.authorization = Utils.AuthRequired.USER
        self.broadcaster_id = broadcaster_id
        self.id = id
        self.start_time = start_time
        self.utc_offset = utc_offset
        self.first = first
        self.after = after
        super().__init__()

class Category:
    id: str
    name: str

class Segment:
    id: str
    start_time: str
    end_time: str
    title: str
    cancelled_until: str
    category: Category
    is_recurring: bool

class Vacation:
    start_time: str
    end_time: str

class Schedule:
    segments: List[Segment]
    broadcacter_id: str
    broadcacter_name: str
    broadcacter_login: str
    vacation: Vacation


class GetChannelStreamScheduleResponse(Utils.PagenationMixin, Utils.ResponseBaseClass):
    def __init__(self) -> None:
        super().__init__(Schedule)

class GetChanneliCalendarRequest(Utils.RequestBaseClass):
    requestType = Utils.HTTPMethod.GET
    scope = None
    authorization = Utils.AuthRequired.CLIENT
    endPoint ="/schedule/icalendar"
    def __init__(self, broadcaster_id: str) -> None:
        self.broadcaster_id = broadcaster_id
        super().__init__()
    
iCal: TypeAlias = str
class GetChanneliCalendarResponse(Utils.ResponseBaseClass):
    def __init__(self) -> None:
        super().__init__(iCal)

class UpdateChannelStreamScheduleRequest(Utils.RequestBaseClass):
    requestType = Utils.HTTPMethod.PATCH
    scope = Scope.Channel.Manage.Schedule
    authorization = Utils.AuthRequired.USER
    endPoint ="/schedule"
    def __init__(self, broadcaster_id: str, is_vacation_enabled: Optional[bool]=None, vacation_start_time: Optional[str]=None, vacation_end_time: Optional[str]=None, timezone: Optional[str]=None) -> None:
        self.broadcaster_id = broadcaster_id
        self.is_vacation_enabled = is_vacation_enabled
        self.vacation_start_time = vacation_start_time
        self.vacation_end_time = vacation_end_time
        self.timezone = timezone
        super().__init__()


class UpdateChannelStreamScheduleResponse(Utils.ResponseBaseClass):
    def __init__(self) -> None:
        super().__init__(None)

class CreateChannelStreamScheduleSegmentRequest(Utils.RequestBaseClass):
    requestType = Utils.HTTPMethod.POST
    scope = Scope.Channel.Manage.Schedule
    authorization = Utils.AuthRequired.USER
    endPoint ="/schedule/segment"
    def __init__(self, broadcaster_id: str, start_time: str, timezone: str, duration: str, is_recurring: Optional[bool]=None, category_id: Optional[str]=None, title: Optional[str]=None) -> None:
        self.broadcaster_id = broadcaster_id
        self.start_time = start_time
        self.timezone = timezone
        self.duration = duration
        self.is_recurring = is_recurring
        self.category_id = category_id
        self.title = title
        super().__init__()
    

class CreateChannelStreamScheduleSegmentResponse(Utils.ResponseBaseClass):
        def __init__(self) -> None:
            super().__init__(Schedule)

class UpdateChannelStreamScheduleSegmentRequest(Utils.RequestBaseClass):
    requestType = Utils.HTTPMethod.PATCH
    scope = Scope.Channel.Manage.Schedule
    authorization = Utils.AuthRequired.USER
    endPoint ="/schedule/segment"
    def __init__(self, broadcaster_id: str, id: str, start_time: Optional[str]=None, duration: Optional[str]=None, 
                 category_id: Optional[str]=None, title: Optional[str]=None, is_canceled: Optional[bool]=None, timezone: Optional[str]=None) -> None:
        self.broadcaster_id = broadcaster_id
        self.id = id
        self.start_time = start_time
        self.duration = duration
        self.category_id = category_id
        self.title = title
        self.is_canceled = is_canceled
        self.timezone = timezone
        super().__init__()
    
class UpdateChannelStreamScheduleSegmentResponse(Utils.ResponseBaseClass):
    def __init__(self) -> None:
        super().__init__(Schedule)

class DeleteChannelStreamScheduleSegmentRequest(Utils.RequestBaseClass):
    requestType = Utils.HTTPMethod.DELETE
    scope = Scope.Channel.Manage.Schedule
    authorization = Utils.AuthRequired.USER
    endPoint ="/schedule/segment"
    def __init__(self, broadcaster_id: str, id: str) -> None:
        self.broadcaster_id = broadcaster_id
        self.id = id
        super().__init__()
    
class DeleteChannelStreamScheduleSegmentResponse(Utils.ResponseBaseClass):
    def __init__(self) -> None:
        super().__init__(None)