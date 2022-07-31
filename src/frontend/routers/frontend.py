from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

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

@app.get("/items/{id}", response_class=HTMLResponse)
async def read_item(request: Request, id: str):
    return templates.TemplateResponse("item.html", context={
        "request": request, 
        "id": id
        },
    )

