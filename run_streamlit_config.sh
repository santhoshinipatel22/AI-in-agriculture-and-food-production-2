#!/bin/bash

echo "🌾 Smart Farming AI - Streamlit Frontend"
echo "======================================="
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found! Install from https://www.python.org/downloads/"
    exit 1
fi

# Create virtual environment if needed
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -q -r requirements_streamlit.txt 2>/dev/null

echo ""
echo "🔧 Configuration"
echo "==============="
echo ""

# Load environment from .env.streamlit
if [ -f ".env.streamlit" ]; then
    echo "✅ Found .env.streamlit"
    export $(cat .env.streamlit | grep -v '^#' | xargs)
    echo "📌 Backend URL: $API_BASE_URL"
else
    echo "⚠️  .env.streamlit not found"
    echo "   Using default: http://localhost:5000"
    export API_BASE_URL="http://localhost:5000"
fi

echo ""

# Check if backend is running
echo "🔍 Checking backend..."
if timeout 2 curl -s "$API_BASE_URL/health" > /dev/null 2>&1; then
    echo "✅ Backend is running at: $API_BASE_URL"
else
    echo "⚠️  Backend not responding at: $API_BASE_URL"
    echo "   You can still use DEMO MODE!"
fi

echo ""
echo "🚀 Starting Streamlit..."
echo "📱 Frontend: http://localhost:8501"
echo "🔌 Backend: $API_BASE_URL"
echo ""
echo "Press Ctrl+C to stop"
echo ""

# Start Streamlit with environment variables
streamlit run streamlit_app.py --server.port=8501 --server.address=localhost
