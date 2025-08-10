import logging
import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import asyncio

class WebServer:
    def __init__(self, buddy, config):
        from fastapi.staticfiles import StaticFiles
        from fastapi.responses import FileResponse
        from fastapi import Request
        self.buddy = buddy
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.app = FastAPI()
        self._setup_routes()
        # Serve static files at root, fallback to index.html for unknown routes
        self.app.mount("/static", StaticFiles(directory="static"), name="static")

        @self.app.get("/")
        async def root():
            return FileResponse("static/index.html")

        @self.app.get("/{full_path:path}")
        async def catch_all(full_path: str, request: Request):
            # Only serve index.html for non-API routes
            if not full_path.startswith("api/"):
                return FileResponse("static/index.html")
            return {"detail": "Not Found"}

    def _setup_routes(self):
        @self.app.post("/api/ask")
        async def ask(request: Request):
            data = await request.json()
            # Support both "input" and "message" keys for flexibility
            user_input = data.get("input", "") or data.get("message", "")
            context = data.get("context", {})
            response = await self.buddy.process_input(user_input, context)
            return JSONResponse(content=response)

        @self.app.get("/api/status")
        async def status():
            status = await self.buddy.get_status()
            return JSONResponse(content=status)

    async def start(self):
        self.logger.info("🌐 Starting BUDDY WebServer on http://127.0.0.1:8000 ...")
        config = uvicorn.Config(self.app, host="127.0.0.1", port=8000, log_level="info")
        server = uvicorn.Server(config)
        await server.serve()
