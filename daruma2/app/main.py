from fastapi import FastAPI, Request, Response
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from typing import List
import uvicorn
import os
from starlette.middleware.sessions import SessionMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
import time

class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, max_requests: int = 100, window_seconds: int = 60):
        super().__init__(app)
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests = {}

    async def dispatch(self, request: Request, call_next):
        client_ip = request.client.host
        current_time = time.time()
        
        # Limpiar solicitudes antiguas
        self.requests = {ip: reqs for ip, reqs in self.requests.items() 
                        if current_time - reqs[-1] < self.window_seconds}
        
        # Verificar límite de velocidad
        if client_ip in self.requests:
            requests = self.requests[client_ip]
            if len(requests) >= self.max_requests:
                if current_time - requests[0] < self.window_seconds:
                    return Response(
                        content="Too many requests",
                        status_code=429
                    )
                requests.pop(0)
            requests.append(current_time)
        else:
            self.requests[client_ip] = [current_time]
        
        response = await call_next(request)
        return response

app = FastAPI(title="Daruma Consulting SRL")

# Security Middleware
# Load config from environment variables
SECRET_KEY = os.getenv("SECRET_KEY", "tu_clave_secreta_aqui_para_desarrollo")
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "*, 127.0.0.1").split(",")
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*").split(",")
CONTACT_EMAIL = os.getenv("CONTACT_EMAIL", "contacto@darumaconsulting.com")
TEAMVIEWER_LINK = os.getenv("TEAMVIEWER_LINK", "https://download.teamviewer.com/download/TeamViewerQS.exe")


app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(TrustedHostMiddleware, allowed_hosts=ALLOWED_HOSTS)
app.add_middleware(GZipMiddleware, minimum_size=1000)
app.add_middleware(RateLimitMiddleware, max_requests=100, window_seconds=60)
app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)

# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Templates configuration
templates = Jinja2Templates(directory="app/templates")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    # Get client's IP from headers or connection info
    client_ip = request.client.host
    context = {
        "request": request,
        "client_ip": client_ip,
        "contact_email": CONTACT_EMAIL,
        "teamviewer_link": TEAMVIEWER_LINK
    }
    return templates.TemplateResponse("index.html", context)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
