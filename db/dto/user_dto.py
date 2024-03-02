from typing import Optional, Any

from pydantic import BaseModel


class UserDto(BaseModel):
    id: Optional[Any] = None
    username: Optional[Any]
    status: Optional[Any]
