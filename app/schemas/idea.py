from pydantic import BaseModel, Field
from typing import Optional, Literal

class IdeaInput(BaseModel):
    idea: str = Field(..., min_length=20, description="User's product/startup idea")
    target_users: str = Field(..., min_length=3, description="Who this idea is for")
    region: Optional[str] = Field(default="Global")
    category: Optional[str] = Field(default="General")
    business_type: Optional[Literal["B2B", "B2C", "B2B2C"]] = Field(default="B2C")
    unique_edge: Optional[str] = Field(default=None, description="What makes it different")