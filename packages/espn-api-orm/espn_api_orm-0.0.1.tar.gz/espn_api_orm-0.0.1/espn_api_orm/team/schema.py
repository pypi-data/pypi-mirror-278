from typing import List, Optional, Any
from espn_api_orm.generic.schema import Ref, Link, Logo
from pydantic import BaseModel, Field

from espn_api_orm.venue.schema import Venue

class TeamRef(BaseModel):
    id: int

class Team(BaseModel):
    ref: Optional[str] = Field(default=None, alias='$ref')
    id: int
    guid: Optional[str] = None
    uid: str
    alternateIds : Optional[dict] = None
    slug: Optional[str] = None
    location: str
    name: Optional[str] = None
    nickname: Optional[str] = None
    abbreviation: Optional[str] = None
    displayName: Optional[str] = None
    shortDisplayName: Optional[str] = None
    color: Optional[str] = None
    alternateColor: Optional[str] = None
    isActive: bool
    isAllStar: Optional[bool] = None
    logo: Optional[str] = None
    logos: Optional[List[Logo]] = None
    links: Optional[List[Link]] = None
    record: Optional[Ref] = None
    oddsRecords: Optional[Ref] = None
    athletes: Optional[Ref] = None
    groups: Optional[Ref] = None
    ranks: Optional[Ref] = None
    statistics: Optional[Ref] = None
    leaders: Optional[Ref] = None
    injuries: Optional[Ref] = None
    notes: Optional[Ref] = None
    againstTheSpreadRecords: Optional[Ref] = None
    franchise: Optional[Ref] = None
    events: Optional[Ref] = None
    college: Optional[Ref] = None
    venue: Optional[Venue] = None
    conferenceId: Optional[int] = None