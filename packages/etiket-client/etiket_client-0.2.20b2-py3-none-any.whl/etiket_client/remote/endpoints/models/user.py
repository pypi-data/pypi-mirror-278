from etiket_client.remote.endpoints.models.utility import convert_time_from_local_to_utc
from etiket_client.remote.endpoints.models.user_base import UserBase, UserRead
from etiket_client.remote.endpoints.models.types import usernamestr, UserType
from etiket_client.remote.endpoints.models.scope import ScopeRead

from typing import Optional, List
from pydantic import BaseModel, EmailStr, Field, field_serializer

import datetime


class UserCreate(UserBase):
    password : str
    
    @field_serializer('disable_on')
    def collected_serialzer(self, disable_on: datetime, _info):
        return convert_time_from_local_to_utc(disable_on)
        
class UserReadWithScopes(UserRead):
    scopes : List[ScopeRead]

class UserUpdate(BaseModel):
    firstname: Optional[str] = Field(default=None)
    lastname: Optional[str] = Field(default=None)
    email: Optional[EmailStr] = Field(default=None)
    password : Optional[str] = Field(default=None)
    
class UserUpdateInternal(UserUpdate):
    disable_on: Optional[datetime.datetime] = Field(default=None)  
    user_type: Optional[UserType] = Field(default=None)
    active : Optional[str] = Field(default=None)
    
    @field_serializer('disable_on')
    def collected_serialzer(self, disable_on: datetime, _info):
        return convert_time_from_local_to_utc(disable_on)
    
class UserLogin(BaseModel):
    username : str
    password : str