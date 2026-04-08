from pydantic import BaseModel
from typing import List

class UserProfile(BaseModel):
    name: str
    allergies: List[str]