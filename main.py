#!/usr/bin/env python3
"""
BUDDY AI Assistant - Main Entry Point
Advanced AI Assistant with NLP, Decision Engine, and Adaptive Learning
"""


import asyncio
import logging
import sys
import os
from pathlib import Path
from dotenv import load_dotenv


# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Load environment variables from .env
load_dotenv(dotenv_path=project_root / '.env')

from core.assistant import BuddyAssistant
from interfaces.web_server import WebServer
from utils.config import Config
from utils.logger import setup_logging

def main():
    """Main entry point for BUDDY AI Assistant"""
    
    # Setup logging
    setup_logging()
    logger = logging.getLogger(__name__)
    
    try:
        # Initialize configuration
        config = Config()
        logger.info("🤖 Starting BUDDY AI Assistant...")
        
        # Initialize BUDDY
        buddy = BuddyAssistant(config)
        
        # Initialize web interface
        web_server = WebServer(buddy, config)
        
        # Start the assistant
        asyncio.run(start_services(buddy, web_server))
        
    except KeyboardInterrupt:
        logger.info("👋 BUDDY AI Assistant shutting down gracefully...")
    except Exception as e:
        logger.error(f"❌ Failed to start BUDDY: {e}")
        sys.exit(1)

async def start_services(buddy: BuddyAssistant, web_server: WebServer):
    """Start all BUDDY services"""
    
    # Initialize BUDDY core
    await buddy.initialize()
    
    # Start web server
    await web_server.start()

if __name__ == "__main__":
    main()
