from pydantic import BaseModel

class SUserCreate(BaseModel):
    username: str
    password: str
    first_name: str = None
    last_name: str = None

class SUserAuth(BaseModel):
    username: str
    password: str
