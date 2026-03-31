"""
Main entry point for Roblox Camera Server
"""

import os
import logging
from app import create_app
from config.config import get_config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
)

logger = logging.getLogger(__name__)


def main():
    """Run the application"""
    
    # Get configuration
    config = get_config()
    
    # Create app
    app = create_app(config)
    
    # Log startup info
    logger.info("=" * 60)
    logger.info("Roblox Camera Server")
    logger.info("=" * 60)
    logger.info(f"Environment: {os.environ.get('FLASK_ENV', 'development')}")
    logger.info(f"Debug: {app.config['DEBUG']}")
    logger.info(f"Host: {app.config['HOST']}")
    logger.info(f"Port: {app.config['PORT']}")
    logger.info(f"CORS Origins: {app.config['CORS_ORIGINS']}")
    logger.info("=" * 60)
    
    # Run server
    app.run(
        host=app.config['HOST'],
        port=app.config['PORT'],
        debug=app.config['DEBUG'],
        threaded=True
    )


if __name__ == '__main__':
    main()
