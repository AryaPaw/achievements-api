from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app import models, schemas

async def create_user(db: AsyncSession, user: schemas.UserCreate):
    db_user = models.User(username=user.username, language=user.language)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

async def get_users(db: AsyncSession):
    result = await db.execute(select(models.User))
    return result.scalars().all()

async def get_achievements(db: AsyncSession):
    result = await db.execute(select(models.Achievement))
    return result.scalars().all()

async def create_achievement(db: AsyncSession, achievement: schemas.AchievementCreate):
    db_achievement = models.Achievement(name=achievement.name, points=achievement.points, description=achievement.description)
    db.add(db_achievement)
    await db.commit()
    await db.refresh(db_achievement)
    return db_achievement

async def assign_achievement_to_user(db: AsyncSession, user_achievement: schemas.UserAchievementCreate):
    db_user_achievement = models.UserAchievement(user_id=user_achievement.user_id, achievement_id=user_achievement.achievement_id, timestamp=datetime.utcnow())
    db.add(db_user_achievement)
    await db.commit()
    await db.refresh(db_user_achievement)
    return db_user_achievement
