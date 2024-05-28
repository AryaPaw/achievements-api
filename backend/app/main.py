from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app import crud, models, schemas
from app.database import engine, get_db
from typing import List

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
    return await crud.get_users(db=db)

@app.get("/achievements/", response_model=List[schemas.Achievement], tags=["Achievements"])
async def read_achievements(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
    return await crud.get_achievements(db=db)

@app.post("/achievements/", response_model=schemas.Achievement, tags=["Achievements"])
async def create_achievement(achievement: schemas.AchievementCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create_achievement(db=db, achievement=achievement)

@app.post("/user-achievements/", response_model=schemas.UserAchievement, tags=["User Achievements"])
async def assign_achievement(user_achievement: schemas.UserAchievementCreate, db: AsyncSession = Depends(get_db)):
    return await crud.assign_achievement_to_user(db=db, user_achievement=user_achievement)

@app.get("/users/{user_id}/achievements/", response_model=List[schemas.UserAchievement], tags=["User Achievements"])
async def get_user_achievements(user_id: int, db: AsyncSession = Depends(get_db)):
    return await crud.get_user_achievements(db=db, user_id=user_id)

@app.get("/statistics/max-achievements", tags=["Statistics"])
async def user_with_max_achievements(db: AsyncSession = Depends(get_db)):
    user = await crud.user_with_max_achievements(db=db)
    if not user:
        raise HTTPException(status_code=404, detail="No user found")
    return {"username": user.username, "achievement_count": user.achievement_count}

@app.get("/statistics/max-points", tags=["Statistics"])
async def user_with_max_points(db: AsyncSession = Depends(get_db)):
    user = await crud.user_with_max_points(db=db)
    if not user:
        raise HTTPException(status_code=404, detail="No user found")
    return {"username": user.username, "total_points": user.total_points}

@app.get("/statistics/max-point-difference", tags=["Statistics"])
async def users_with_max_point_difference(db: AsyncSession = Depends(get_db)):
    max_user, min_user = await crud.users_with_max_point_difference(db=db)
    if not max_user or not min_user:
        raise HTTPException(status_code=404, detail="No users found")
    max_diff = max_user.total_points - min_user.total_points
    return {"users": (max_user.username, min_user.username), "point_difference": max_diff}

@app.get("/statistics/consistent-achievements", tags=["Statistics"])
async def users_with_consistent_achievements(db: AsyncSession = Depends(get_db)):
    consistent_users = await crud.users_with_consistent_achievements(db=db)
    if not consistent_users:
        raise HTTPException(status_code=404, detail="No consistent users found")
    return {"consistent_users": consistent_users}
