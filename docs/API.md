# API Documentation

Complete API reference for Roblox Camera Server.

## Base URL

```
http://localhost:5000/api
```

## Authentication

All endpoints (except `/health`) require token-based authentication.

### Header Format
```
Authorization: Bearer {TOKEN}
```

### Tokens

- **Roblox Token**: Used by Roblox game scripts
- **Frontend Token**: Used by web frontend

## Endpoints

### Health Check

Check if server is running.

```
GET /health
```

**Response (200 OK):**
```json
{
  "status": "ok",
  "timestamp": "2024-01-01T12:00:00.000000",
  "version": "1.0.0"
}
```

---

### Get System Status

Get current system status and commands.

```
GET /status
Authorization: Bearer {ROBLOX_TOKEN}
```

**Response (200 OK):**
```json
{
  "has_frame": true,
  "commands": {
    "pan_tilt_x": 0.5,
    "pan_tilt_y": -0.3,
    "move_x": 0.2,
    "move_z": 0.8
  },
  "timestamp": "2024-01-01T12:00:00.000000"
}
```

**Errors:**
- `401 Unauthorized` - Invalid or missing token

---

### Upload Frame

Receive camera frame from Roblox.

```
POST /frame/upload
Authorization: Bearer {ROBLOX_TOKEN}
Content-Type: application/json
```

**Request Body:**
```json
{
  "frame": "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg==",
  "timestamp": "2024-01-01T12:00:00Z",
  "camera_position": {
    "x": 0,
    "y": 5,
    "z": 0
  },
  "camera_rotation": {
    "x": 0,
    "y": 0,
    "z": 0
  }
}
```

**Response (200 OK):**
```json
{
  "status": "received",
  "commands": {
    "pan_tilt_x": 0.0,
    "pan_tilt_y": 0.0,
    "move_x": 0.0,
    "move_z": 0.0
  }
}
```

**Errors:**
- `400 Bad Request` - Missing frame data
- `401 Unauthorized` - Invalid token
- `413 Payload Too Large` - Frame exceeds max size

---

### Get Frame

Retrieve current camera frame (Frontend).

Frame is deleted after retrieval.

```
GET /frame/get
Authorization: Bearer {FRONTEND_TOKEN}
```

**Response (200 OK):**
```json
{
  "data": "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg==",
  "timestamp": "2024-01-01T12:00:00Z",
  "camera_position": {
    "x": 0,
    "y": 5,
    "z": 0
  },
  "camera_rotation": {
    "x": 0,
    "y": 0,
    "z": 0
  }
}
```

**Response (200 OK - No Frame):**
```json
{
  "frame": null
}
```

**Errors:**
- `401 Unauthorized` - Invalid token

---

### Set Commands

Send camera control commands (Frontend).

```
POST /commands/set
Authorization: Bearer {FRONTEND_TOKEN}
Content-Type: application/json
```

**Request Body:**
```json
{
  "pan_tilt_x": 0.5,
  "pan_tilt_y": -0.3,
  "move_x": 0.2,
  "move_z": 0.8
}
```

**Notes:**
- All values are clamped to range [-1.0, 1.0]
- Only include fields you want to update
- Partial updates are supported

**Response (200 OK):**
```json
{
  "status": "ok"
}
```

**Errors:**
- `400 Bad Request` - Missing command data
- `401 Unauthorized` - Invalid token

---

### Get Commands

Retrieve current camera control commands (Roblox).

```
GET /commands/get
Authorization: Bearer {ROBLOX_TOKEN}
```

**Response (200 OK):**
```json
{
  "pan_tilt_x": 0.5,
  "pan_tilt_y": -0.3,
  "move_x": 0.2,
  "move_z": 0.8
}
```

**Errors:**
- `401 Unauthorized` - Invalid token

---

### Reset Commands

Reset all commands to zero.

```
POST /commands/reset
Authorization: Bearer {FRONTEND_TOKEN}
```

**Response (200 OK):**
```json
{
  "status": "ok"
}
```

**Errors:**
- `401 Unauthorized` - Invalid token

---

## Error Responses

All error responses follow this format:

```json
{
  "error": "Error message"
}
```

### Common Status Codes

| Code | Meaning |
|------|---------|
| 200 | OK - Request successful |
| 400 | Bad Request - Invalid request data |
| 401 | Unauthorized - Invalid/missing token |
| 403 | Forbidden - Access denied |
| 404 | Not Found - Endpoint doesn't exist |
| 413 | Payload Too Large - Frame exceeds max size |
| 500 | Internal Server Error - Server error |

---

## Command Values

### Pan/Tilt (Camera Rotation)

- **pan_tilt_x**: Horizontal pan (-1.0 to 1.0)
  - Negative: Pan left
  - Positive: Pan right
  
- **pan_tilt_y**: Vertical tilt (-1.0 to 1.0)
  - Negative: Tilt down
  - Positive: Tilt up

### Movement (Camera Position)

- **move_x**: Left/Right movement (-1.0 to 1.0)
  - Negative: Move left
  - Positive: Move right
  
- **move_z**: Forward/Backward movement (-1.0 to 1.0)
  - Negative: Move backward
  - Positive: Move forward

---

## Rate Limiting

Currently no rate limiting is implemented. For production, consider:

1. Implementing rate limiting middleware
2. Using API gateway with rate limiting
3. Monitoring for abuse

---

## CORS

CORS is enabled for all origins by default. Configure via:

```
CORS_ORIGINS=https://yourdomain.com,https://another.com
```

---

## Examples

### cURL

**Upload Frame:**
```bash
curl -X POST http://localhost:5000/api/frame/upload \
  -H "Authorization: Bearer roblox_secret_token_12345" \
  -H "Content-Type: application/json" \
  -d '{
    "frame": "base64_data",
    "timestamp": "2024-01-01T12:00:00Z",
    "camera_position": {"x": 0, "y": 5, "z": 0},
    "camera_rotation": {"x": 0, "y": 0, "z": 0}
  }'
```

**Get Commands:**
```bash
curl http://localhost:5000/api/commands/get \
  -H "Authorization: Bearer roblox_secret_token_12345"
```

**Set Commands:**
```bash
curl -X POST http://localhost:5000/api/commands/set \
  -H "Authorization: Bearer frontend_secret_token_12345" \
  -H "Content-Type: application/json" \
  -d '{
    "pan_tilt_x": 0.5,
    "pan_tilt_y": -0.3,
    "move_x": 0.2,
    "move_z": 0.8
  }'
```

### Python

```python
import requests

BASE_URL = "http://localhost:5000/api"
ROBLOX_TOKEN = "roblox_secret_token_12345"
FRONTEND_TOKEN = "frontend_secret_token_12345"

# Get commands
response = requests.get(
    f"{BASE_URL}/commands/get",
    headers={"Authorization": f"Bearer {ROBLOX_TOKEN}"}
)
commands = response.json()

# Set commands
requests.post(
    f"{BASE_URL}/commands/set",
    headers={"Authorization": f"Bearer {FRONTEND_TOKEN}"},
    json={
        "pan_tilt_x": 0.5,
        "pan_tilt_y": -0.3,
        "move_x": 0.2,
        "move_z": 0.8
    }
)
```

### JavaScript

```javascript
const BASE_URL = "http://localhost:5000/api";
const FRONTEND_TOKEN = "frontend_secret_token_12345";

// Set commands
async function setCommands(commands) {
  const response = await fetch(`${BASE_URL}/commands/set`, {
    method: "POST",
    headers: {
      "Authorization": `Bearer ${FRONTEND_TOKEN}`,
      "Content-Type": "application/json"
    },
    body: JSON.stringify(commands)
  });
  return response.json();
}

// Get frame
async function getFrame() {
  const response = await fetch(`${BASE_URL}/frame/get`, {
    headers: {
      "Authorization": `Bearer ${FRONTEND_TOKEN}`
    }
  });
  return response.json();
}
```

---

## Versioning

Current API version: **1.0.0**

Future versions will maintain backward compatibility when possible.

---

## Support

For issues or questions about the API:
- Check this documentation
- Review code examples
- Open an issue on GitHub
