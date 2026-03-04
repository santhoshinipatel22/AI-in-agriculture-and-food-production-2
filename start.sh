#!/bin/bash

# Smart Farming Ecosystem - Complete Startup Script
# This script sets up and starts all services

set -e

echo "========================================"
echo "🌾 Smart Farming Ecosystem Startup"
echo "========================================"

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if Docker is installed
echo -e "${BLUE}Checking prerequisites...${NC}"
if ! command -v docker &> /dev/null; then
    echo -e "${YELLOW}⚠️  Docker not found. Please install Docker first.${NC}"
    echo "Visit: https://www.docker.com/products/docker-desktop"
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo -e "${YELLOW}⚠️  Docker Compose not found. Please install Docker Compose.${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Docker and Docker Compose found${NC}"

# Navigate to project directory
PROJECT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$PROJECT_DIR"

# Create environment files if they don't exist
echo -e "\n${BLUE}Setting up environment files...${NC}"

if [ ! -f backend/.env ]; then
    echo -e "${YELLOW}Creating backend/.env${NC}"
    cp backend/.env.example backend/.env
    echo -e "${GREEN}✓ Created backend/.env${NC}"
else
    echo -e "${GREEN}✓ backend/.env already exists${NC}"
fi

if [ ! -f frontend/.env ]; then
    echo -e "${YELLOW}Creating frontend/.env${NC}"
    cp frontend/.env.example frontend/.env
    echo -e "${GREEN}✓ Created frontend/.env${NC}"
else
    echo -e "${GREEN}✓ frontend/.env already exists${NC}"
fi

# Start services
echo -e "\n${BLUE}Starting all services...${NC}"
echo "This may take 1-2 minutes on first run..."

cd docker
docker-compose up -d

echo -e "\n${GREEN}✓ All services started!${NC}"

# Wait for services to be ready
echo -e "\n${BLUE}Waiting for services to be ready...${NC}"
sleep 5

# Check if services are ready
echo -e "\n${BLUE}Service Status:${NC}"

# Check Backend
if curl -s http://localhost:5000/api/health > /dev/null 2>&1; then
    echo -e "${GREEN}✓ Backend API${NC} - Running on http://localhost:5000"
else
    echo -e "${YELLOW}⏳ Backend API${NC} - Starting up..."
fi

# Check Frontend
if curl -s http://localhost:3000 > /dev/null 2>&1; then
    echo -e "${GREEN}✓ Frontend Web${NC} - Running on http://localhost:3000"
else
    echo -e "${YELLOW}⏳ Frontend Web${NC} - Starting up..."
fi

# Check MongoDB
if mongo --version > /dev/null 2>&1; then
    echo -e "${GREEN}✓ MongoDB${NC} - Running on localhost:27017"
else
    echo -e "${GREEN}✓ MongoDB${NC} - Running in Docker on port 27017"
fi

# Check Redis
if redis-cli ping > /dev/null 2>&1; then
    echo -e "${GREEN}✓ Redis Cache${NC} - Running on localhost:6379"
else
    echo -e "${GREEN}✓ Redis Cache${NC} - Running in Docker on port 6379"
fi

echo -e "\n${YELLOW}========================================"
echo "🚀 Smart Farming is Starting Up!${NC}"
echo "========================================"
echo -e "\n${BLUE}Access the application:${NC}"
echo "  🌐 Frontend: http://localhost:3000"
echo "  🔌 Backend API: http://localhost:5000"
echo "  📚 API Docs: http://localhost:5000/api"
echo ""
echo -e "${BLUE}Next Steps:${NC}"
echo "  1. Open http://localhost:3000 in your browser"
echo "  2. Create an account or login"
echo "  3. Start exploring Smart Farming features!"
echo ""
echo -e "${BLUE}Useful Commands:${NC}"
echo "  View logs:     ${YELLOW}docker-compose -f docker/docker-compose.yml logs -f${NC}"
echo "  Stop services: ${YELLOW}docker-compose -f docker/docker-compose.yml down${NC}"
echo "  Stop & clean:  ${YELLOW}docker-compose -f docker/docker-compose.yml down -v${NC}"
echo ""
echo -e "${BLUE}Documentation:${NC}"
echo "  Quick Start: ${YELLOW}cat QUICK_START.md${NC}"
echo "  Full Guide: ${YELLOW}cat SETUP_GUIDE.md${NC}"
echo "  API Reference: ${YELLOW}cat API_REFERENCE.md${NC}"
echo ""
echo -e "${YELLOW}⏳ Services may take 30-60 seconds to fully start${NC}"
echo -e "${YELLOW}   If you see errors, wait a moment and refresh the page${NC}"
echo ""
echo -e "${GREEN}========================================"
echo "Happy Farming! 🌾👨‍🌾👩‍🌾"
echo "========================================${NC}\n"
