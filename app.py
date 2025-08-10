#!/usr/bin/env python3
"""
Production startup script for BUDDY AI Assistant
Optimized for web hosting platforms like Render, Railway, Heroku
"""
import os
import sys
import asyncio
import logging
from pathlib import Path

# Setup paths
sys.path.append(str(Path(__file__).parent))

# Import BUDDY components
from core.assistant import BuddyAssistant
from interfaces.web_server import WebServer
from utils.config import Config

async def main():
    """Main application entry point for production"""
    # Setup logging for production
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    logger = logging.getLogger(__name__)
    logger.info("🚀 Starting BUDDY AI Assistant in production mode...")
    
    try:
        # Initialize configuration
        config = Config()
        logger.info("✅ Configuration loaded")
        
        # Initialize BUDDY Assistant
        buddy = BuddyAssistant(config)
        await buddy.initialize()
        logger.info("✅ BUDDY AI Assistant initialized")
        
        # Get port from environment (for hosting platforms)
        port = int(os.environ.get("PORT", 8000))
        host = "0.0.0.0"  # Bind to all interfaces for hosting
        
        # Initialize and start web server
        web_server = WebServer(buddy, config)
        
        # Update the web server to use environment port
        import uvicorn
        logger.info(f"🌐 Starting web server on {host}:{port}")
        
        config_uvicorn = uvicorn.Config(
            web_server.app, 
            host=host, 
            port=port, 
            log_level="info"
        )
        server = uvicorn.Server(config_uvicorn)
        await server.serve()
        
    except Exception as e:
        logger.error(f"❌ Failed to start BUDDY AI Assistant: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 BUDDY AI Assistant stopped by user")
    except Exception as e:
        print(f"💥 Fatal error: {e}")
        sys.exit(1)
