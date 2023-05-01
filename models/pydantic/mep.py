from typing import List
from pydantic import BaseModel, Field


# Pydantic classes
class CommitteeIn(BaseModel):
    name: str


class CommitteeOut(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class ActivityIn(BaseModel):
    description: str


class ActivityOut(BaseModel):
    id: int
    description: str
    mep_id: int

    class Config:
        orm_mode = True


class MEPIn(BaseModel):
    name: str = Field(
        ..., description="The full name of the Member of the European Parliament (MEP)."
    )
    affiliation: str = Field(
        ..., description="The political group or affiliation to which the MEP belongs."
    )
    activities: List[ActivityIn] = Field(
        ...,
        description="A list of activities or roles that the MEP is involved in, such as voting, proposing initiatives, or attending events.",
    )
    committees: List[CommitteeIn] = Field(
        ...,
        description="A list of parliamentary committees that the MEP is a member of or is attending.",
    )
    source_url: str


class MEPOut(BaseModel):
    id: int
    name: str
    affiliation: str
    source_url: str

    class Config:
        orm_mode = True
