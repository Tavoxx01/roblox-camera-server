"""
Configuration settings for Roblox Camera Server
"""

import os
from datetime import timedelta


class Config:
    """Base configuration"""
    
    # Flask settings
    DEBUG = False
    TESTING = False
    
    # Security
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    
    # Authentication tokens
    ROBLOX_TOKEN = os.environ.get('ROBLOX_TOKEN', 'roblox_secret_token_12345')
    FRONTEND_TOKEN = os.environ.get('FRONTEND_TOKEN', 'frontend_secret_token_12345')
    
    # Server settings
    HOST = os.environ.get('HOST', '0.0.0.0')
    PORT = int(os.environ.get('PORT', 5000))
    
    # CORS settings
    CORS_ORIGINS = os.environ.get('CORS_ORIGINS', '*').split(',')
    
    # Frame settings
    FRAME_TIMEOUT = int(os.environ.get('FRAME_TIMEOUT', 30))  # seconds
    MAX_FRAME_SIZE = int(os.environ.get('MAX_FRAME_SIZE', 10 * 1024 * 1024))  # 10MB
    
    # Command settings
    COMMAND_TIMEOUT = int(os.environ.get('COMMAND_TIMEOUT', 5))  # seconds


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False


class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False
    # Ensure tokens are set in production
    ROBLOX_TOKEN = os.environ.get('ROBLOX_TOKEN')
    FRONTEND_TOKEN = os.environ.get('FRONTEND_TOKEN')


class TestingConfig(Config):
    """Testing configuration"""
    DEBUG = True
    TESTING = True
    ROBLOX_TOKEN = 'test_roblox_token'
    FRONTEND_TOKEN = 'test_frontend_token'


def get_config():
    """Get configuration based on environment"""
    env = os.environ.get('FLASK_ENV', 'development')
    
    if env == 'production':
        return ProductionConfig
    elif env == 'testing':
        return TestingConfig
    else:
        return DevelopmentConfig
