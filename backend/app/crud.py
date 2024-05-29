from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func
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

async def get_user_achievements(db: AsyncSession, user_id: int):
    result = await db.execute(
        select(models.UserAchievement).where(models.UserAchievement.user_id == user_id)
    )
    return result.scalars().all()

async def user_with_max_achievements(db: AsyncSession):
    result = await db.execute(
        select(models.User.username, func.count(models.UserAchievement.id).label('achievement_count'))
        .join(models.UserAchievement)
        .group_by(models.User.username)
        .order_by(func.count(models.UserAchievement.id).desc())
        .limit(1)
    )
    return result.fetchone()

async def user_with_max_points(db: AsyncSession):
    result = await db.execute(
        select(models.User.username, func.sum(models.Achievement.points).label('total_points'))
        .select_from(models.User)
        .join(models.UserAchievement)
        .join(models.Achievement)
        .group_by(models.User.username)
        .order_by(func.sum(models.Achievement.points).desc())
        .limit(1)
    )
    return result.fetchone()

async def users_with_max_point_difference(db: AsyncSession):
    result = await db.execute(
        select(models.User.username, func.sum(models.Achievement.points).label('total_points'))
        .select_from(models.User)
        .join(models.UserAchievement)
        .join(models.Achievement)
        .group_by(models.User.username)
    )
    users = result.all()
    users.sort(key=lambda x: x.total_points, reverse=True)
    return users[0], users[-1]

async def users_with_min_point_difference(db: AsyncSession):
    result = await db.execute(
        select(models.User.username, func.sum(models.Achievement.points).label('total_points'))
        .select_from(models.User)
        .join(models.UserAchievement)
        .join(models.Achievement)
        .group_by(models.User.username)
    )
    users = result.all()
    if len(users) < 2:
        return None, None
    users.sort(key=lambda x: x.total_points)
    return users[0], users[1]


async def users_with_consistent_achievements(db: AsyncSession):
    result = await db.execute(
        select(models.User.username, models.UserAchievement.timestamp)
        .select_from(models.User)
        .join(models.UserAchievement)
        .order_by(models.User.username, models.UserAchievement.timestamp)
    )
    user_achievements = result.fetchall()

    consistent_users = []
    current_user = user_achievements[0].username
    dates = [user_achievements[0].timestamp]

    for achievement in user_achievements[1:]:
        if achievement.username == current_user:
            dates.append(achievement.timestamp)
        else:
            if len(dates) >= 7 and all(dates[i] - dates[i-1] == timedelta(days=1) for i in range(1, 7)):
                consistent_users.append(current_user)
            current_user = achievement.username
            dates = [achievement.timestamp]

    return consistent_users
