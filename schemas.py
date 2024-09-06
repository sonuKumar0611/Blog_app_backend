from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    password: str
    user_type: str

class UserUpdate(BaseModel):
    username: str
    user_type: str

class BlogCreate(BaseModel):
    title: str
    body: str
    username: str
    visibility: str

class BlogUpdate(BaseModel):
    title: str
    body: str
    visibility: str
    file_path: str

