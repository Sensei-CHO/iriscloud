import os
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from src import lxdlib, grapher
load_dotenv()

lxd = lxdlib.Cloud(os.getenv("lxd_endpoint"), os.getenv("lxd_cert"), os.getenv("lxd_key"), project="Iris-Infra")
fastapp = FastAPI()

fastapp.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@fastapp.get("/", response_class=HTMLResponse)
async def root(request: Request):
    datas = {"request": request, "graph": grapher.Graph(lxd, "300px", "100%", "#868686").draw()}
    return templates.TemplateResponse("index.html", datas)

@fastapp.get("/todo", response_class=HTMLResponse)
async def todo(request: Request):
    datas = {"request": request}
    return templates.TemplateResponse("todo.html", datas)

@fastapp.get("/diagram", response_class=HTMLResponse)
async def diagram():
    return grapher.Graph(lxd, "100%", "100%", "white").draw()
    # return templates.TemplateResponse("index.html", datas)