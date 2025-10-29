from pydantic import BaseModel
from typing import List

class Resume(BaseModel):
    text: str

class SkillsResponse(BaseModel):
    skills: List[str]
