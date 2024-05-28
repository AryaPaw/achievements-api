from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func
from app import crud, models, schemas
from app.database import engine, get_db
from typing import List
from datetime import datetime, timedelta

app = FastAPI(
    title="Achievements API",
    description="API для работы с достижениями",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)

@app.get("/health", tags=["Health"])
async def health_check():
    return {"status": "ok"}

@app.post("/users/", response_model=schemas.User, tags=["Users"])
async def create_user(user: schemas.UserCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create_user(db=db, user=user)

@app.get("/users/", response_model=List[schemas.User], tags=["Users"])
async def read_users(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
    users = await crud.get_users(db=db)
    return users

@app.get("/achievements/", response_model=List[schemas.Achievement], tags=["Achievements"])
async def read_achievements(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
    achievements = await crud.get_achievements(db=db)
    return achievements

@app.post("/achievements/", response_model=schemas.Achievement, tags=["Achievements"])
async def create_achievement(achievement: schemas.AchievementCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create_achievement(db=db, achievement=achievement)

@app.post("/user-achievements/", response_model=schemas.UserAchievement, tags=["User Achievements"])
async def assign_achievement(user_achievement: schemas.UserAchievementCreate, db: AsyncSession = Depends(get_db)):
    return await crud.assign_achievement_to_user(db=db, user_achievement=user_achievement)

@app.get("/users/{user_id}/achievements/", response_model=List[schemas.UserAchievement], tags=["User Achievements"])
async def get_user_achievements(user_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(models.UserAchievement).where(models.UserAchievement.user_id == user_id)
    )
    user_achievements = result.scalars().all()
    return user_achievements

@app.get("/statistics/max-achievements", tags=["Statistics"])
async def user_with_max_achievements(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(models.User.username, func.count(models.UserAchievement.id).label('achievement_count'))
        .join(models.UserAchievement)
        .group_by(models.User.username)
        .order_by(func.count(models.UserAchievement.id).desc())
        .limit(1)
    )
    user = result.fetchone()
    if not user:
        raise HTTPException(status_code=404, detail="No user found")
    return {"username": user.username, "achievement_count": user.achievement_count}

@app.get("/statistics/max-points", tags=["Statistics"])
async def user_with_max_points(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(models.User.username, func.sum(models.Achievement.points).label('total_points'))
        .select_from(models.User)
        .join(models.UserAchievement)
        .join(models.Achievement)
        .group_by(models.User.username)
        .order_by(func.sum(models.Achievement.points).desc())
        .limit(1)
    )
    user = result.fetchone()
    if not user:
        raise HTTPException(status_code=404, detail="No user found")
    return {"username": user.username, "total_points": user.total_points}

@app.get("/statistics/max-point-difference", tags=["Statistics"])
async def users_with_max_point_difference(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(models.User.username, func.sum(models.Achievement.points).label('total_points'))
        .select_from(models.User)
        .join(models.UserAchievement)
        .join(models.Achievement)
        .group_by(models.User.username)
    )
    users = result.all()
    if not users:
        raise HTTPException(status_code=404, detail="No users found")
    users.sort(key=lambda x: x.total_points, reverse=True)
    max_diff_users = (users[0].username, users[-1].username)
    max_diff = users[0].total_points - users[-1].total_points
    return {"users": max_diff_users, "point_difference": max_diff}

@app.get("/statistics/consistent-achievements", tags=["Statistics"])
async def users_with_consistent_achievements(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(models.User.username, models.UserAchievement.timestamp)
        .select_from(models.User)
        .join(models.UserAchievement)
        .order_by(models.User.username, models.UserAchievement.timestamp)
    )
    user_achievements = result.fetchall()
    if not user_achievements:
        raise HTTPException(status_code=404, detail="No user achievements found")

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

    return {"consistent_users": consistent_users}
