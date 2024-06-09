import base64
from typing import Optional
import jwt
from datetime import datetime
class JWTGenerator:
    """
     {
  "exp": 1484242525,
  "opaque_user_id": "UG12X345T6J78",
  "channel_id": "test_channel",
  "role": "broadcaster",
  "is_unlinked": "false",
  "pubsub_perms": {
    "listen": [ "broadcast", "whisper-UG12X345T6J78" ],
    "send": ["broadcast","whisper-*"]
  }
}

    _extended_summary_
    """
    def __init__(self,  secret:base64 ) -> None:
        self.secret = secret.encode('utf-8')

    def generate(self, channel_id:str, exp: datetime, is_unlinked: bool, pubsub_perms: dict, role:str, user_id:Optional[str]=None, opaque_user_id:Optional[str]=None):

        payload: dict = {}
        payload["exp"] = exp   
        payload["channel_id"] = channel_id
        payload["role"] = role
        payload["is_unlinked"] = is_unlinked
        payload["pubsub_perms"] = pubsub_perms
        if user_id is not None:
            payload["user_id"] = user_id
        if opaque_user_id is not None:
            payload["opaque_user_id"] = opaque_user_id
        return jwt.encode(payload, self.secret, algorithm='HS256')
    
