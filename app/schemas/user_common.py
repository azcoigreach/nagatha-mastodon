from pydantic import BaseModel

class UserIdentifierIn(BaseModel):
    username: str 