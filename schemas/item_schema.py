from pydantic import BaseModel
from typing import Optional

# This schema is used for request validation and response formatting
class ItemSchema(BaseModel):
    id: int
    name: str
    description: Optional[str] = None

    class Config:
        orm_mode = True
