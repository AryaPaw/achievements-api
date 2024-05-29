from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class UserBase(BaseModel):
    username: str
    language: str

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int

    class Config:
        from_attributes = True

class AchievementBase(BaseModel):
    name: str
    points: int
    description: str

class AchievementCreate(AchievementBase):
    pass

class Achievement(AchievementBase):
    id: int

    class Config:
        from_attributes = True

class UserAchievementBase(BaseModel):
    user_id: int
    achievement_id: int

class UserAchievementCreate(UserAchievementBase):
    pass

class UserAchievement(UserAchievementBase):
    id: int
    timestamp: datetime

    class Config:
        from_attributes = True

class MaxAchievementsResponse(BaseModel):
    username: str
    achievement_count: int

class MaxPointsResponse(BaseModel):
    username: str
    total_points: int

class PointDifferenceResponse(BaseModel):
    users: List[str]
    point_difference: int

class ConsistentAchievementsResponse(BaseModel):
    consistent_users: List[str]
