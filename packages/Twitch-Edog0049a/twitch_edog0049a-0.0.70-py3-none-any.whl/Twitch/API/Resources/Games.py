from Twitch.API.Resources.__imports import *

class GetTopGamesRequest(Utils.RequestBaseClass):
	requestType = Utils.HTTPMethod.GET
	scope = None
	authorization = Utils.AuthRequired.CLIENT
	endPoint = "games/top"
	def __init__(self, first: int = 20, after: Optional[str]=None, before: Optional[str]=None, userAuth: bool=False) -> None:
		self.first = first
		self.after = after
		self.before = before
		if userAuth:
			self.authorization = Utils.AuthRequired.USER
		super().__init__()
        
class Game:
	id: str
	name: str	
	box_art_url: str
	igdb_id: str

class GetTopGamesResponse(Utils.ResponseBaseClass):
	def __init__(self) -> None:
		super().__init__(Game)

class GetGamesRequest(Utils.RequestBaseClass):
	requestType = Utils.HTTPMethod.GET
	scope = None
	authorization = Utils.AuthRequired.CLIENT
	endPoint = "/games"
	def __init__(self, id: Optional[List[str]]=None, name: Optional[List[str]]=None, igdb_id: Optional[List[str]]=None ,userAuth: bool=False) -> None:
		self.id = id
		self.name = name
		self.igdb_id = igdb_id
		if userAuth:
			self.authorization = Utils.AuthRequired.USER
		super().__init__()

class GetGamesResponse(Utils.ResponseBaseClass):
        def __init__(self) -> None:
            super().__init__(Game)