'''
    main.py

    Author: Abraham Horta

    Purpose: This file serves as the main entry point for the Secure Transactional API system.
    It initializes the FastAPI application, configures static files and Jinja2 templates for frontend
    rendering, and connects all authentication and transaction routes.
    It also serves as the bridge between the backend API and the web-based frontend interface.

    Sources: The following code was inspired/influenced by the following
    -- sources, but adapted and altered for the API project.

    1. https://fastapi.tiangolo.com/advanced/templates/
    2. https://fastapi.tiangolo.com/reference/templating/
    3. https://blog.logrocket.com/server-side-rendering-with-fastapi-and-mysql/

'''

from fastapi import FastAPI
from user_routes import router as user_router
from transaction_routes import router as transaction_router
# -- The following imports are for the Frontend/UI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import Request

app = FastAPI()

# -- Template/Static Setup for Frontend
app.mount("/static", StaticFiles(directory = "static"), name = "static")
templates = Jinja2Templates(directory = "templates")

# -- For including route files
app.include_router(user_router)
app.include_router(transaction_router)

# -- Updated/Replaced Root Route (For Loading Frontend page When Visiting: http://127.0.0.1:8000/)
@app.get("/", response_class = HTMLResponse)
def home(request: Request):
    return (templates.TemplateResponse
        (
            request = request,
            name = "index.html",
            context = {}
        ))






