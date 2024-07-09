from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi_pagination import add_pagination

from smart_vendor.routers.users import router as users_router
from smart_vendor.routers.user_accounts import router as user_accounts_router
from smart_vendor.routers.payments import router as payments_router

app = FastAPI(title="Smart Vendor APIs", version="v1.0")


@app.get("/", name="docs", include_in_schema=False)
async def root():
    return RedirectResponse("/docs")


app.include_router(user_accounts_router, tags=["accounts"])
app.include_router(users_router, tags=["users"])
app.include_router(payments_router, tags=["payment"])
add_pagination(app)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
