from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates


from frontend.routers.api.projects import get_project_by_id

templates = Jinja2Templates(directory="src/templates")


app.mount("/static", StaticFiles(directory="src/static"), name="static")

# @router.get(
#     "/home",
#     response_class=HTMLResponse,
# )
# async def get_all_releases(request: Request):
#     return templates.TemplateResponse(

#         "portfolio/home.html",
#         context={
#             "request": request,
#             "testing": "Hello World"
#         },
#     )


@router.get(
    "/project/{project_id}",
    response_class=HTMLResponse,
)
async def home_page(project_id: int, request: Request, db: Session = Depends(get_db)):
    db_project = get_project_by_id(db, project_id=project_id)
    segment = get_segment(request)
    return templates.TemplateResponse(
        "portfolio/project.html",
        context={"request": request, "segment": segment, "project": db_project},
    )


@app.get("/items/{id}", response_class=HTMLResponse)
async def read_item(request: Request, id: str, db: dependds):
    return templates.TemplateResponse("item.html", {"request": request, "id": id})
