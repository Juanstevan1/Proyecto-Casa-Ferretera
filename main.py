from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static") 
template = Jinja2Templates(directory="templates")


@app.get("/")
def index(req: Request):
    return template.TemplateResponse(
        name = "index.html",
        context = {"request": req}
    )
    
async def root():
    return 