# Deployment Guide

This guide covers deploying the Roblox Camera Server to various platforms.

## Local Development

```bash
python run.py
```

Server runs at `http://localhost:5000`

## Railway (Recommended)

Railway is the easiest option for Python/Flask deployment.

### Steps:

1. **Install Railway CLI**
   ```bash
   npm i -g @railway/cli
   ```

2. **Login to Railway**
   ```bash
   railway login
   ```

3. **Initialize project**
   ```bash
   railway init
   ```

4. **Set environment variables**
   ```bash
   railway variables set FLASK_ENV=production
   railway variables set ROBLOX_TOKEN=your_token
   railway variables set FRONTEND_TOKEN=your_token
   ```

5. **Deploy**
   ```bash
   railway up
   ```

Your app will be available at the Railway URL provided.

## Render

### Steps:

1. **Connect GitHub repository** to Render
2. **Create new Web Service**
3. **Configure:**
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn -w 4 -b 0.0.0.0:$PORT "app:create_app()"`
4. **Set Environment Variables:**
   - `FLASK_ENV=production`
   - `ROBLOX_TOKEN=your_token`
   - `FRONTEND_TOKEN=your_token`
5. **Deploy**

## Vercel (Frontend + Serverless Backend)

Vercel can host both frontend and backend as serverless functions.

### Steps:

1. **Install Vercel CLI**
   ```bash
   npm i -g vercel
   ```

2. **Deploy**
   ```bash
   vercel
   ```

3. **Set environment variables** in Vercel dashboard

## PythonAnywhere

### Steps:

1. **Upload code** to PythonAnywhere
2. **Create Web App** with Flask
3. **Configure WSGI file:**
   ```python
   from app import create_app
   application = create_app()
   ```
4. **Set environment variables** in Web App settings
5. **Reload Web App**

## Heroku (Legacy)

Heroku now requires paid plans, but the setup is similar:

```bash
heroku login
heroku create your-app-name
git push heroku main
heroku config:set ROBLOX_TOKEN=your_token
heroku config:set FRONTEND_TOKEN=your_token
```

## Docker Deployment

### Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV FLASK_ENV=production
ENV HOST=0.0.0.0
ENV PORT=5000

EXPOSE 5000

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:create_app()"]
```

### Build and Run

```bash
docker build -t roblox-camera-server .
docker run -p 5000:5000 \
  -e ROBLOX_TOKEN=your_token \
  -e FRONTEND_TOKEN=your_token \
  roblox-camera-server
```

## Environment Variables

For production, set these environment variables:

```
FLASK_ENV=production
ROBLOX_TOKEN=your_secure_roblox_token
FRONTEND_TOKEN=your_secure_frontend_token
SECRET_KEY=your_secure_secret_key
CORS_ORIGINS=https://yourdomain.com
```

## Monitoring

### Health Check
```bash
curl https://your-deployment-url/api/health
```

### Logs
- Railway: `railway logs`
- Render: Dashboard → Logs
- Vercel: Dashboard → Logs
- PythonAnywhere: Web App → Error/Server logs

## Troubleshooting

### "Module not found" errors
- Ensure `requirements.txt` is installed
- Check Python version compatibility

### "Connection refused"
- Verify server is running
- Check port configuration
- Verify firewall settings

### CORS errors
- Update `CORS_ORIGINS` environment variable
- Ensure frontend URL is in allowed origins

### Token authentication fails
- Verify tokens are set correctly
- Check token format in requests
- Ensure tokens match between frontend and backend

## Performance Tips

1. **Use Gunicorn with multiple workers**
   ```bash
   gunicorn -w 4 -b 0.0.0.0:5000 "app:create_app()"
   ```

2. **Enable gzip compression**
   - Most platforms do this automatically

3. **Monitor memory usage**
   - In-memory storage grows with frames
   - Consider adding cleanup mechanisms

4. **Use CDN for static files**
   - If serving frontend from backend

## Security Checklist

- [ ] Change default tokens
- [ ] Use HTTPS/TLS
- [ ] Set strong SECRET_KEY
- [ ] Restrict CORS origins
- [ ] Enable rate limiting
- [ ] Monitor logs for suspicious activity
- [ ] Keep dependencies updated
- [ ] Use environment variables for secrets

## Next Steps

1. Deploy backend to your chosen platform
2. Update frontend API URL to point to deployed backend
3. Deploy frontend to Vercel or similar
4. Test end-to-end integration
5. Monitor logs and performance
