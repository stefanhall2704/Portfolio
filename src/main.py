import secure
import uvicorn
from fastapi import BackgroundTasks, Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import (
    get_redoc_html,
    get_swagger_ui_html,
    get_swagger_ui_oauth2_redirect_html,
)
from fastapi.openapi.utils import get_openapi
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from starlette.requests import Request
from starlette.responses import JSONResponse, RedirectResponse

app = FastAPI(
    # swagger_ui_oauth2_redirect_url="/oauth2-redirect",
    swagger_ui_oauth2_redirect_url=None,
    redoc_url=None,
    docs_url=None,
    openapi_url=None,
)





# @app.on_event("startup")
# async def load_config() -> None:
#     """
#     Load OpenID config on startup.
#     """
#     await azure_pkce_scheme.openid_config.load_config()



app.mount("/static", StaticFiles(directory="src/static"), name="static")


@app.get("/", response_class=RedirectResponse, include_in_schema=False)
async def redirect_to_login():
    return RedirectResponse("/home")


@app.get(
    "/openapi.json",
    include_in_schema=False,
)
async def get_open_api_endpoint():
    return JSONResponse(
        get_openapi(title="Stefan's Portfolio - OpenAPI", version=1, routes=app.routes)
    )


@app.get(
    "/redoc", include_in_schema=False)
async def redoc_html():
    return get_redoc_html(
        openapi_url=app.openapi_url,
        title="Stefan's Portfolio - Redoc",
    )


@app.middleware("http")
async def redirect_if_needed(request: Request, call_next):
    response = await call_next(request)
    if response.status_code == 403 and "/api/" not in str(request.url):
        response = RedirectResponse(f"/login?redirect={request.url}")
    return response


secure_headers = secure.Secure()


@app.middleware("http")
async def set_secure_headers(request, call_next):
    response = await call_next(request)
    secure_headers.framework.fastapi(response)
    return response


@app.middleware("http")
async def set_cache_control_header_on_static_files(request: Request, call_next):
    response = await call_next(request)
    if "/static" in str(request.url):
        response.headers["Cache-Control"] = "private"
    return response


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
