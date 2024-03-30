from fastapi import FastAPI

from smart_vendor.database import Base, engine
from smart_vendor.routers.users import router as users_router
from smart_vendor.routers.user_accounts import router as user_accounts_router

app = FastAPI()

app.include_router(users_router, tags=["users"])
app.include_router(user_accounts_router, tags=["accounts"])

if __name__ == "__main__":
    import uvicorn
    Base.metadata.create_all(engine)
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
