#!/bin/bash

echo "🌾 Smart Farming AI - Streamlit Deployment"
echo "==========================================="
echo ""

# Check Python version
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed!"
    echo "Install from: https://www.python.org/downloads/"
    exit 1
fi

echo "✅ Python $(python3 --version) detected"
echo ""

# Create virtual environment if not exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -q -r requirements_streamlit.txt

echo ""
echo "✅ Setup complete!"
echo ""

# Retrieve backend status
echo "🔍 Checking backend API..."
if curl -s http://localhost:5000/health > /dev/null 2>&1; then
    echo "✅ Backend is running at http://localhost:5000"
else
    echo "⚠️  Backend is NOT running at http://localhost:5000"
    echo "   Make sure to start the backend first:"
    echo "   cd backend && npm start"
fi

echo ""
echo "🚀 Starting Streamlit app..."
echo "📱 Your app will open at: http://localhost:8501"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Start Streamlit
streamlit run streamlit_app.py --server.port=8501 --server.address=localhost

