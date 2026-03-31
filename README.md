# Roblox Camera Server

Backend server for Roblox Security Camera System - A real-time camera control system for Roblox games.

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Flask 2.3](https://img.shields.io/badge/flask-2.3-green.svg)](https://flask.palletsprojects.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Features

- 🎥 **Real-time Frame Streaming** - Receive camera frames from Roblox
- 🎮 **Bidirectional Control** - Send camera commands back to Roblox
- 🔐 **Token Authentication** - Secure API with token-based auth
- 📦 **Thread-safe Storage** - In-memory frame and command storage
- 🚀 **Production Ready** - Gunicorn compatible, CORS enabled
- 📝 **Well Documented** - Comprehensive API documentation

## Architecture

```
Roblox Game
    ↓ (POST /api/frame/upload)
Python Flask Server
    ↓ (GET /api/frame/get)
Frontend (HTML/JS)
    ↓ (POST /api/commands/set)
Python Flask Server
    ↓ (GET /api/commands/get)
Roblox Game
```

## Quick Start

### Prerequisites

- Python 3.8+
- pip (Python package manager)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/Tavoxx01/roblox-camera-server.git
cd roblox-camera-server
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set environment variables (optional):
```bash
export FLASK_ENV=development
export ROBLOX_TOKEN=your_roblox_token
export FRONTEND_TOKEN=your_frontend_token
export PORT=5000
```

5. Run the server:
```bash
python run.py
```

Server will start at `http://localhost:5000`

## API Endpoints

### Health Check
```
GET /api/health
```

### Frame Upload (Roblox)
```
POST /api/frame/upload
Authorization: Bearer {ROBLOX_TOKEN}

{
  "frame": "base64_encoded_image",
  "timestamp": "2024-01-01T12:00:00Z",
  "camera_position": {"x": 0, "y": 5, "z": 0},
  "camera_rotation": {"x": 0, "y": 0, "z": 0}
}
```

### Get Frame (Frontend)
```
GET /api/frame/get
Authorization: Bearer {FRONTEND_TOKEN}
```

### Set Commands (Frontend)
```
POST /api/commands/set
Authorization: Bearer {FRONTEND_TOKEN}

{
  "pan_tilt_x": 0.5,
  "pan_tilt_y": -0.3,
  "move_x": 0.2,
  "move_z": 0.8
}
```

### Get Commands (Roblox)
```
GET /api/commands/get
Authorization: Bearer {ROBLOX_TOKEN}
```

### System Status
```
GET /api/status
Authorization: Bearer {ROBLOX_TOKEN}
```

## Configuration

Configuration is managed through environment variables:

| Variable | Default | Description |
|----------|---------|-------------|
| `FLASK_ENV` | development | Environment (development/production/testing) |
| `HOST` | 0.0.0.0 | Server host |
| `PORT` | 5000 | Server port |
| `ROBLOX_TOKEN` | roblox_secret_token_12345 | Roblox authentication token |
| `FRONTEND_TOKEN` | frontend_secret_token_12345 | Frontend authentication token |
| `CORS_ORIGINS` | * | Allowed CORS origins |
| `FRAME_TIMEOUT` | 30 | Frame timeout in seconds |
| `MAX_FRAME_SIZE` | 10485760 | Maximum frame size (10MB) |

## Project Structure

```
roblox-camera-server/
├── app/
│   ├── __init__.py          # Application factory
│   ├── auth.py              # Authentication decorators
│   ├── errors.py            # Error handlers
│   ├── routes.py            # API routes
│   └── storage.py           # In-memory storage
├── config/
│   ├── __init__.py
│   └── config.py            # Configuration classes
├── tests/                   # Unit tests
├── docs/                    # Documentation
├── run.py                   # Entry point
├── requirements.txt         # Python dependencies
├── .gitignore              # Git ignore rules
└── README.md               # This file
```

## Development

### Running Tests
```bash
python -m pytest tests/
```

### Code Style
```bash
python -m flake8 app/
python -m black app/
```

### Running with Gunicorn (Production)
```bash
gunicorn -w 4 -b 0.0.0.0:5000 "app:create_app()"
```

## Deployment

### Vercel (Frontend only)
The frontend can be deployed to Vercel. Update the API URL in your frontend code to point to your backend server.

### Railway
```bash
railway login
railway init
railway up
```

### Render
1. Connect your GitHub repository
2. Create a new Web Service
3. Set build command: `pip install -r requirements.txt`
4. Set start command: `gunicorn -w 4 -b 0.0.0.0:$PORT "app:create_app()"`

### PythonAnywhere
1. Upload your code
2. Create a web app with Flask
3. Configure WSGI file to use `app:create_app()`

## Security

⚠️ **Important Security Notes:**

1. **Change default tokens** in production
2. **Use HTTPS** in production
3. **Set strong SECRET_KEY** environment variable
4. **Validate all inputs** before processing
5. **Use environment variables** for sensitive data
6. **Enable CORS only for trusted origins** in production

## Troubleshooting

### "Unauthorized" errors
- Check that your token is correct
- Verify token format: `Authorization: Bearer {token}`
- Ensure token matches configured value

### Frame not received
- Check Roblox script is sending frames
- Verify server is running on correct port
- Check firewall/network settings

### CORS errors
- Update `CORS_ORIGINS` environment variable
- Ensure frontend URL is in allowed origins

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For issues, questions, or suggestions:
- Open an [Issue](https://github.com/Tavoxx01/roblox-camera-server/issues)
- Check existing documentation
- Review API examples

## Related Projects

- [Roblox Camera Client](https://github.com/Tavoxx01/roblox-camera-client) - Frontend and Lua scripts
- [LAC Online](https://github.com/Tavoxx01) - Main project

## Changelog

### v1.0.0 (2026-03-31)
- Initial release
- Frame upload/retrieval
- Command control system
- Token-based authentication
- CORS support

---

**Made with ❤️ for Roblox developers**
