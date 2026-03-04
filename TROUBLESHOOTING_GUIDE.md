# Smart Farming Ecosystem - Troubleshooting Guide

This comprehensive troubleshooting guide covers the most common issues and their solutions.

## Table of Contents
1. [Installation Issues](#installation-issues)
2. [Docker Issues](#docker-issues)
3. [Backend Issues](#backend-issues)
4. [Frontend Issues](#frontend-issues)
5. [Database Issues](#database-issues)
6. [API Issues](#api-issues)
7. [Authentication Issues](#authentication-issues)
8. [Performance Issues](#performance-issues)
9. [ML Model Issues](#ml-model-issues)
10. [Deployment Issues](#deployment-issues)
11. [Getting Further Help](#getting-further-help)

---

## Installation Issues

### Problem: npm packages won't install
**Symptoms**: `npm install` fails with permission or compatibility errors

**Solutions**:
```bash
# Clear npm cache
npm cache clean --force

# Remove node_modules and package-lock.json
rm -rf node_modules package-lock.json

# Reinstall
npm install

# If still failing, try with sudo (not recommended but last resort)
sudo npm install
```

### Problem: Python packages installation fails
**Symptoms**: `pip install -r requirements.txt` gives errors

**Solutions**:
```bash
# Update pip
pip install --upgrade pip

# Install with verbose output to see what's failing
pip install -r requirements.txt -v

# Try installing packages individually
pip install tensorflow scikit-learn opencv-python flask

# Use a virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Problem: Node.js version incompatibility
**Symptoms**: `npm start` fails saying wrong Node version

**Solutions**:
```bash
# Check current Node version
node --version

# Should be v18.0.0 or higher
# If not, install/update Node.js from https://nodejs.org/

# On macOS with Homebrew
brew install node

# On Ubuntu
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs
```

---

## Docker Issues

### Problem: Docker containers won't start
**Symptoms**: `docker-compose up` fails or containers exit immediately

**Solutions**:
```bash
# Check what went wrong
docker-compose logs

# Get detailed logs for specific service
docker-compose logs backend
docker-compose logs frontend

# Rebuild without cache
docker-compose build --no-cache

# Start with verbose output
docker-compose --verbose up

# If still failing, clean everything
docker-compose down -v
docker system prune -a
docker-compose up -d
```

### Problem: Port already in use
**Symptoms**: "Address already in use" error when starting services

**Solutions**:
```bash
# Windows - Find and kill process on port 5000
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# macOS/Linux - Find and kill process
lsof -ti:5000 | xargs kill -9
lsof -ti:3000 | xargs kill -9

# Or change ports in docker-compose.yml
# Change "5000:5000" to "5001:5000" to use 5001 instead
```

### Problem: Docker can't connect to MongoDB/Redis
**Symptoms**: Backend can't connection to database from within container

**Solutions**:
```bash
# Ensure services are running
docker-compose ps

# Check if services are healthy
docker inspect mongodb | grep -A 10 "State"

# Restart specific service
docker-compose restart mongodb

# Check network connectivity
docker network ls
docker network inspect docker_default

# View all service logs
docker-compose logs
```

### Problem: Out of disk space for Docker volumes
**Symptoms**: Containers crash or won't start, disk full errors

**Solutions**:
```bash
# Clean up Docker
docker system prune -a --volumes

# This removes:
# - All stopped containers
# - All images not used by running containers
# - All dangling volumes
# - All dangling networks

# Or be selective
docker container prune
docker image prune
docker volume prune
```

---

## Backend Issues

### Problem: Backend won't start (npm start fails)
**Symptoms**: `npm start` returns errors

**Solutions**:
```bash
# Check for syntax errors
npm run lint

# Check if all dependencies are installed
npm ls

# Reinstall dependencies
rm -rf node_modules package-lock.json
npm install

# Try running with verbose logging
NODE_DEBUG=* npm start

# Check server.js for port conflicts
# Ensure PORT is set correctly in .env
```

### Problem: Can't connect to MongoDB
**Symptoms**: "MongoDb connection failed" error in logs

**Solutions**:
```bash
# Check if MongoDB is running
# Docker
docker ps | grep mongodb

# Local
mongosh --eval "db.version()"

# Check connection string in .env
# Should be: mongodb://localhost:27017/smart_farming

# Test connection
mongosh mongodb://localhost:27017/test

# If using MongoDB Atlas (cloud), ensure:
# - Network access whitelisted (0.0.0.0/0)
# - Correct username/password in connection string
# - Connection string format: mongodb+srv://user:pass@cluster.mongodb.net/dbname

# Check MongoDB logs
docker logs mongodb
```

### Problem: Redis connection issues
**Symptoms**: "Redis connection refused" or redis not available

**Solutions**:
```bash
# Check if Redis is running
redis-cli ping
# Should return: PONG

# If not running, start it
# Docker
docker run -d -p 6379:6379 redis:7.0

# macOS
brew services start redis

# Linux
sudo systemctl start redis-server

# Test from Node.js
node -e "const redis = require('redis'); const client = redis.createClient(); client.ping((err, reply) => console.log(reply));"
```

### Problem: JWT token errors
**Symptoms**: "Invalid token" or "Token expired" errors

**Solutions**:
```bash
# Check JWT_SECRET in .env
# Should be at least 32 characters
# Generate new secret:
node -e "console.log(require('crypto').randomBytes(32).toString('hex'))"

# Add to .env
JWT_SECRET=your-new-secret-here

# Restart backend server
npm start

# Clear browser local storage to force re-login
# Browser DevTools → Application → Local Storage → Clear All
```

### Problem: CORS errors when frontend calls backend
**Symptoms**: "Access to XMLHttpRequest has been blocked by CORS policy"

**Solutions**:
```bash
# Check CORS_ORIGINS in backend .env
# Should include frontend URL
CORS_ORIGINS=http://localhost:3000,http://localhost:3001

# Ensure CORS middleware is enabled in server.js
const cors = require('cors');
app.use(cors({
  origin: process.env.CORS_ORIGINS.split(','),
  credentials: true
}));

# Restart backend
npm start

# Clear browser cache and try again
```

### Problem: File upload fails
**Symptoms**: Image upload returns error

**Solutions**:
```bash
# Check MAX_FILE_SIZE in .env
# Default: 5242880 (5MB)
MAX_FILE_SIZE=10485760  # 10MB

# Ensure uploads directory exists
mkdir -p backend/uploads

# Check file permissions
chmod -R 755 backend/uploads

# Check disk space
df -h

# Restart backend
npm start
```

---

## Frontend Issues

### Problem: npm start won't work
**Symptoms**: `npm start` fails or React doesn't load

**Solutions**:
```bash
# Clear React cache
rm -rf node_modules .cache
npm cache clean --force
npm install

# Check for syntax errors
npm test

# Start with verbose output
npm start -- --verbose

# Check .env file
# REACT_APP_API_URL must match backend URL
cat frontend/.env
```

### Problem: "Cannot find module" errors
**Symptoms**: Module not found errors for imports

**Solutions**:
```bash
# Ensure all dependencies are installed
npm install

# Check import paths are correct (case-sensitive on Linux!)
# ❌ Wrong: import Component from './component'
# ✅ Correct: import Component from './Component'

# Clear build cache
rm -rf build
npm run build
```

### Problem: API calls return 404
**Symptoms**: Frontend can't reach backend endpoints

**Solutions**:
```bash
# Check REACT_APP_API_URL in frontend/.env
# Should match backend URL
cat frontend/.env

# Test backend is running
curl http://localhost:5000/api/health

# Check browser network tab for exact error
# DevTools → Network → Filter for failed requests

# Check CORS settings in backend
echo $CORS_ORIGINS  # Should include http://localhost:3000

# Restart both services
npm start  # frontend
# And in another terminal
npm start  # backend
```

### Problem: CSS styles not loading
**Symptoms**: Page looks broken, no styling

**Solutions**:
```bash
# Check that CSS files exist
ls frontend/src/pages/*.css

# Hard refresh browser
Ctrl+Shift+R (or Cmd+Shift+R on Mac)

# Clear browser cache
DevTools → Application → Cache Storage → Clear All

# Check CSS imports in JSX are correct
// ✅ Correct
import './Dashboard.css'

// Check no typos in class names
```

### Problem: Can't login even with correct credentials
**Symptoms**: Login fails with error message

**Solutions**:
```bash
# Check backend is running and healthy
curl http://localhost:5000/api/health

# Verify user exists in database
mongosh smart_farming
db.farmers.find({email: "your-email@test.com"})

# Check logs for error details
# In another terminal, watch backend logs
docker-compose logs -f backend

# Clear local storage and try again
# DevTools → Application → Local Storage → Delete smart_farming entry

# Test API manually
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"user@test.com","password":"pass"}'
```

---

## Database Issues

### Problem: MongoDB not accessible
**Symptoms**: Can't connect to MongoDB database

**Solutions**:
```bash
# Check if MongoDB is running
docker ps | grep mongodb

# Start MongoDB if not running
docker run -d -p 27017:27017 --name mongodb mongo:6.0

# Test connection
mongosh mongodb://localhost:27017

# Check MongoDB logs
docker logs mongodb

# Ensure correct URI in .env
MONGODB_URI=mongodb://localhost:27017/smart_farming

# For MongoDB Atlas (cloud)
# Connection string should be:
MONGODB_URI=mongodb+srv://username:password@cluster0.mongodb.net/smart_farming?retryWrites=true&w=majority
```

### Problem: Database corruption or queries failing
**Symptoms**: "Unexpected end of JSON input" or database errors

**Solutions**:
```bash
# Connect to MongoDB
mongosh smart_farming

# Check database status
db.version()

# Detect and repair database
db.repairDatabase()

# Drop and recreate database (WARNING - deletes all data!)
db.dropDatabase()

# After repair, restart backend
npm start
```

### Problem: Data not persisting after restart
**Symptoms**: Data is lost when MongoDB restarts

**Solutions**:
```bash
# Ensure MongoDB volume is properly mounted
# In docker-compose.yml:
volumes:
  - mongodb_data:/data/db

# Check volume exists
docker volume ls | grep mongodb

# Inspect volume
docker inspect mongodb_data

# If volume issues, recreate
docker-compose down -v
docker-compose up -d

# Data will be empty, so you may need to re-seed
```

### Problem: Slow database queries
**Symptoms**: Slow page loads, timeout errors

**Solutions**:
```bash
# Check MongoDB indexes
mongosh smart_farming
db.crops.getIndexes()

# Add missing indexes
db.crops.createIndex({farmerId: 1})
db.crops.createIndex({status: 1})

# Check slow queries
db.setProfilingLevel(1)  # Profile slow queries
db.system.profile.find().pretty()

# Analyze query plan
db.crops.find({farmerId: "123"}).explain("executionStats")
```

---

## API Issues

### Problem: API returns 500 error
**Symptoms**: "Internal Server Error" on API calls

**Solutions**:
```bash
# Check backend logs for error details
docker-compose logs backend

# Ensure all dependencies are installed
npm list

# Check environment variables are set
echo $MONGODB_URI
echo $JWT_SECRET

# Test API with curl or Postman
curl http://localhost:5000/api/health

# Check database connectivity
# Error details usually in logs

# Common causes:
# - Missing environment variable
# - Database connection failed
# - Syntax error in code
```

### Problem: API returns 401 Unauthorized
**Symptoms**: "Unauthorized" or "Invalid token" errors

**Solutions**:
```bash
# Ensure JWT token is being sent
# Headers must include:
Authorization: Bearer YOUR_TOKEN

# Verify token is valid
# Frontend should store it in localStorage

# Check JWT secret matches
# Backend and frontend should use same secret

# Test authentication
curl -X GET http://localhost:5000/api/crops \
  -H "Authorization: Bearer YOUR_TOKEN"

# Generate new token via login
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"user@test.com","password":"pass"}'
```

### Problem: File upload endpoint fails
**Symptoms**: Multipart form data upload returns error

**Solutions**:
```bash
# Ensure form is multipart/form-data
# ✅ Correct
fetch('/api/diseases/detect/cropId', {
  method: 'POST',
  body: formData  // FormData object
})

# ❌ Wrong
fetch('/api/diseases/detect/cropId', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: formData
})

# Check file size
# MAX_FILE_SIZE in .env (default 5MB)

# Check uploads directory has write permission
chmod 755 backend/uploads

# Test with curl
curl -F "image=@path/to/image.jpg" \
  http://localhost:5000/api/diseases/detect/CROPID \
  -H "Authorization: Bearer TOKEN"
```

---

## Authentication Issues

### Problem: Tokens expire frequently
**Symptoms**: "Token expired" errors shortly after login

**Solutions**:
```bash
# Check token expiration settings in .env
JWT_EXPIRE=7d       # Access token (should be short)
JWT_REFRESH_EXPIRE=30d  # Refresh token (should be long)

# Update if needed
JWT_EXPIRE=24h  # 24 hours
JWT_REFRESH_EXPIRE=7d  # 7 days

# Restart backend
npm start

# Frontend must implement token refresh logic
```

### Problem: Can't refresh token
**Symptoms**: Refresh token endpoint returns error

**Solutions**:
```bash
# Ensure refresh token is valid
# It should be stored in localStorage/sessionStorage

# Check /auth/refresh-token endpoint
curl -X POST http://localhost:5000/api/auth/refresh-token \
  -H "Content-Type: application/json" \
  -d '{"refreshToken":"your-refresh-token"}'

# Verify token format is correct
# Should be a JWT token (three parts separated by dots)

# Check JWT_REFRESH_SECRET in .env
echo $JWT_REFRESH_SECRET

# If tokens are corrupted, user must login again
```

---

## Performance Issues

### Problem: Slow API responses
**Symptoms**: API requests take >5 seconds

**Solutions**:
```bash
# Check server load
top  # Or Task Manager on Windows

# Check network latency
ping localhost

# Enable caching
# In Redis, cache frequently accessed data
# Check priceService.js for caching patterns

# Add database indexes (see Database Issues section)

# Check for N+1 queries in code
# Use .populate() in Mongoose queries

# Monitor with logs
npm run dev  # Shows timing info
```

### Problem: High memory usage
**Symptoms**: Backend crashes with out of memory errors

**Solutions**:
```bash
# Check memory usage
docker stats

# Limit container memory in docker-compose.yml
services:
  backend:
    mem_limit: 1g  # 1GB limit

# Identify memory leaks
# Check for unclosed database connections

# Restart service
docker-compose restart backend

# Clear cache periodically
redis-cli FLUSHDB
```

### Problem: Frontend is slow
**Symptoms**: Pages take long to load

**Solutions**:
```bash
# Build optimized version
npm run build

# Check bundle size
npm install -g webpack-bundle-analyzer
npm run analyze

# Optimize large lists with pagination
# Check Dashboard.jsx for list optimization

# Enable lazy loading for routes
import { lazy, Suspense } from 'react'
const Dashboard = lazy(() => import('./pages/Dashboard'))

# Use React DevTools Profiler to find slow components
```

---

## ML Model Issues

### Problem: Python script won't run
**Symptoms**: Python ML model files return errors

**Solutions**:
```bash
# Ensure Python is installed
python --version  # Should be 3.8+

# Check dependencies
pip list | grep tensorflow

# Install missing packages
pip install -r requirements.txt

# Run with verbose output
python ml-models/disease-detection/disease_detection_model.py -v

# Check for import errors
python -c "import tensorflow as tf; print(tf.__version__)"
```

### Problem: Disease detection returns wrong predictions
**Symptoms**: Model predicts wrong disease

**Solutions**:
```bash
# The models are mock implementations
# They need to be trained with real data

# To improve accuracy:
1. Collect real disease images
2. Label them properly
3. Use the training script to train model
4. Deploy updated model

# For now, use for testing/demo purposes

# Check model confidence score
# If < 80%, consider as low confidence
```

---

## Deployment Issues

### Problem: Docker build fails
**Symptoms**: `docker build` returns errors

**Solutions**:
```bash
# Build with no cache
docker build --no-cache -f backend/Dockerfile ./backend

# View full build output
docker build --progress=plain ./backend

# Check Dockerfile for errors
# Common issues:
# - Missing base image
# - Incorrect paths
# - Missing files

# Example: correct Dockerfile
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
EXPOSE 5000
CMD ["npm", "start"]
```

### Problem: Container crashes after deployment
**Symptoms**: Container runs then immediately stops

**Solutions**:
```bash
# Check logs
docker logs CONTAINER_ID

# Common causes:
# - Missing environment variables
# - Database not accessible
# - Port already in use
# - Application error

# Run container interactively to debug
docker run -it -p 5000:5000 image_name /bin/bash

# Ensure all env vars are set
docker run -e MONGODB_URI=mongodb://... -e JWT_SECRET=... image_name

# Check application starts properly
docker run --entrypoint node image_name src/server.js --help
```

---

## Getting Further Help

### 1. Check Documentation
- [QUICK_START.md](./QUICK_START.md) - Quick fixes
- [SETUP_GUIDE.md](./SETUP_GUIDE.md) - Detailed setup help
- [DEVELOPMENT_WORKFLOW.md](./DEVELOPMENT_WORKFLOW.md) - Development issues
- [API_REFERENCE.md](./API_REFERENCE.md) - API issues
- [COMPREHENSIVE_README.md](./COMPREHENSIVE_README.md) - Feature documentation

### 2. Gather Information
When seeking help, provide:
```
- Error message (complete)
- Last 20 lines of relevant logs
- Environment details (OS, Node version, Python version)
- Steps to reproduce
- What you've already tried
```

### 3. Check Logs
```bash
# Backend logs
docker-compose logs backend
npm start  # Shows logs directly

# Frontend logs
Chrome DevTools Console (F12)

# MongoDB logs
docker-compose logs mongodb

# All services
docker-compose logs
```

### 4. Common Quick Fixes
```bash
# 1. Restart everything
docker-compose down
docker-compose up -d

# 2. Clear cache
npm cache clean --force
docker system prune -a

# 3. Reinstall dependencies
rm -rf node_modules package-lock.json
npm install

# 4. Update .env files
cp .env.example .env
# Edit with correct values

# 5. Check if services are running
docker-compose ps
curl http://localhost:5000/api/health
```

### 5. Still Need Help?
1. Review error messages carefully (often contain solution)
2. Check documentation index: [DOCUMENTATION_INDEX.md](./DOCUMENTATION_INDEX.md)
3. Review your .env files for missing/incorrect values
4. Check GitHub issues for similar problems
5. Review application logs for specific error details

---

**Remember**: Most issues are related to:
1. Missing/incorrect environment variables
2. Services not running (MongoDB, Redis, Backend)
3. Port conflicts
4. Missing dependencies
5. Incorrect configuration

Check these first!

---

**Happy troubleshooting! 🔧**

**Last Updated**: 2024
**Version**: 1.0.0
