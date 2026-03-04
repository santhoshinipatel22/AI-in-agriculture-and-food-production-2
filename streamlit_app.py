import streamlit as st
import requests
import json
from datetime import datetime, timedelta
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from PIL import Image
import io
import base64

# Page config
st.set_page_config(
    page_title="🌾 Smart Farming AI",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS styling
st.markdown("""
    <style>
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    </style>
    """, unsafe_allow_html=True)

# API Configuration
import os

# Get API URL from environment variable or use default
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:5000")
API_URL = f"{API_BASE_URL}/api"

# Session State
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user = None
    st.session_state.token = None

# ============================================
# 1. AUTHENTICATION PAGE
# ============================================
def login_page():
    st.title("🌾 Smart Farming AI System")
    
    # Backend status check
    try:
        requests.get(f"{API_URL.replace('/api', '')}/health", timeout=2)
        backend_running = True
    except:
        backend_running = False
    
    if not backend_running:
        st.warning("""
        ⚠️ **Backend API is not running**
        
        To enable full features (registration, login, disease detection, real weather, prices, etc.):
        
        ```bash
        cd backend
        npm install
        npm start
        ```
        
        For now, you can use **Demo Mode** below to explore the UI! 👇
        """)
        
        col1, col2, col3 = st.columns(3)
        with col2:
            if st.button("🟢 DEMO MODE", use_container_width=True):
                st.session_state.logged_in = True
                st.session_state.user = {
                    "id": "demo",
                    "name": "Demo Farmer",
                    "email": "demo@farm.com",
                    "phone": "9876543210"
                }
                st.session_state.token = "demo_token"
                st.success("✅ Demo mode activated! You can explore the UI now.")
                st.rerun()
        st.divider()
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### Login")
        login_email = st.text_input("Email", key="login_email")
        login_password = st.text_input("Password", type="password", key="login_password")
        
        if st.button("Login", use_container_width=True, type="primary"):
            try:
                response = requests.post(
                    f"{API_URL}/auth/login",
                    json={"email": login_email, "password": login_password},
                    timeout=10
                )
                if response.status_code == 200:
                    data = response.json()
                    st.session_state.logged_in = True
                    st.session_state.user = data.get("user")
                    st.session_state.token = data.get("accessToken")
                    st.success("✅ Logged in successfully!")
                    st.rerun()
                else:
                    st.error("❌ Invalid credentials")
            except requests.exceptions.ConnectionError:
                st.error("❌ Backend not running!\n\nStart the backend with:\n```bash\ncd backend\nnpm start\n```")
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
    
    with col2:
        st.markdown("### Register")
        reg_name = st.text_input("Full Name", key="reg_name")
        reg_email = st.text_input("Email", key="reg_email")
        reg_password = st.text_input("Password", type="password", key="reg_password")
        reg_phone = st.text_input("Phone", key="reg_phone")
        
        if st.button("Register", use_container_width=True, type="primary"):
            try:
                response = requests.post(
                    f"{API_URL}/auth/register",
                    json={
                        "name": reg_name,
                        "email": reg_email,
                        "password": reg_password,
                        "phone": reg_phone
                    },
                    timeout=10
                )
                if response.status_code == 201:
                    st.success("✅ Account created! Please login.")
                else:
                    st.error(f"Error: {response.json().get('message', 'Registration failed')}")
            except requests.exceptions.ConnectionError:
                st.error("❌ Backend not running!\n\n**To enable registration:**\n```bash\ncd backend\nnpm install\nnpm start\n```\n\nFor now, you can use Demo Mode!")
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")

# ============================================
# 2. DASHBOARD PAGE
# ============================================
def dashboard_page():
    st.title("📊 Dashboard")
    
    try:
        headers = {"Authorization": f"Bearer {st.session_state.token}"}
        
        # Fetch metrics
        try:
            response = requests.get(f"{API_URL}/crops/metrics", headers=headers, timeout=10)
            metrics = response.json() if response.status_code == 200 else None
        except:
            metrics = None
        
        # Demo data if backend is down
        if metrics is None:
            st.info("📌 **Demo Mode** - Showing sample data")
            metrics = {
                "activeCrops": 3,
                "totalYield": 4500,
                "totalExpense": 15000,
                "diseaseAlerts": 1
            }
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("🌱 Active Crops", metrics.get("activeCrops", 0))
        with col2:
            st.metric("📈 Total Yield (kg)", f"{metrics.get('totalYield', 0):,.0f}")
        with col3:
            st.metric("💰 Total Expense", f"₹{metrics.get('totalExpense', 0):,.0f}")
        with col4:
            st.metric("⚠️ Disease Alerts", metrics.get("diseaseAlerts", 0))
        
        st.divider()
        
        # Crop Management Tabs
        tab1, tab2, tab3 = st.tabs(["📋 My Crops", "➕ Add Crop", "📊 Analytics"])
        
        with tab1:
            st.subheader("Your Crops")
            try:
                crops_response = requests.get(f"{API_URL}/crops", headers=headers, timeout=10)
                crops = crops_response.json() if crops_response.status_code == 200 else None
            except:
                crops = None
            
            if crops is None:
                # Mock crops for demo
                crops = [
                    {"_id": "1", "name": "Rice", "type": "Rice", "area": 2.5, "status": "Growing"},
                    {"_id": "2", "name": "Wheat", "type": "Wheat", "area": 3.0, "status": "Germination"},
                    {"_id": "3", "name": "Cotton", "type": "Cotton", "area": 1.5, "status": "Growing"},
                ]
                st.dataframe(pd.DataFrame(crops), use_container_width=True)
            else:
                if crops:
                    df = pd.DataFrame(crops)
                    st.dataframe(df, use_container_width=True)
                else:
                    st.info("No crops added yet. Add your first crop!")
        
        with tab2:
            st.subheader("Add New Crop")
            with st.form("add_crop_form"):
                crop_name = st.text_input("Crop Name")
                crop_type = st.selectbox("Crop Type", ["Wheat", "Rice", "Corn", "Cotton", "Sugarcane", "Soybean"])
                area = st.number_input("Area (acres)", min_value=0.1)
                sowing_date = st.date_input("Sowing Date")
                
                if st.form_submit_button("Add Crop", use_container_width=True):
                    try:
                        add_response = requests.post(
                            f"{API_URL}/crops",
                            json={
                                "name": crop_name,
                                "type": crop_type,
                                "area": area,
                                "sowingDate": sowing_date.isoformat()
                            },
                            headers=headers,
                            timeout=10
                        )
                        if add_response.status_code == 201:
                            st.success("✅ Crop added successfully!")
                            st.rerun()
                        else:
                            st.error("Failed to add crop")
                    except:
                        st.success("✅ Crop added! (Demo Mode)")
        
        with tab3:
            st.subheader("Crop Analytics")
            chart_data = pd.DataFrame({
                "Date": pd.date_range(start="2024-01-01", periods=30),
                "Growth": range(30, 60)
            })
            fig = px.line(chart_data, x="Date", y="Growth", title="Crop Growth Progress")
            st.plotly_chart(fig, use_container_width=True)
    
    except Exception as e:
        st.error(f"Error: {str(e)}")

# ============================================
# 3. DISEASE DETECTION PAGE
# ============================================
def disease_detection_page():
    st.title("🦠 Disease Detection (AI)")
    
    headers = {"Authorization": f"Bearer {st.session_state.token}"}
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("Upload Crop Image")
        uploaded_file = st.file_uploader("Choose an image", type=["jpg", "jpeg", "png", "webp"])
        
        if uploaded_file:
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Image", use_container_width=True)
            
            try:
                crop_list_response = requests.get(f"{API_URL}/crops", headers=headers, timeout=10)
                crops = crop_list_response.json() if crop_list_response.status_code == 200 else []
            except:
                crops = [{"_id": "1", "name": "Rice"}, {"_id": "2", "name": "Wheat"}]
            
            crop_ids = [c.get("_id", c.get("id")) for c in crops]
            
            if crop_ids:
                selected_crop = st.selectbox("Select Crop", crop_ids)
                
                if st.button("🔍 Detect Disease", use_container_width=True, type="primary"):
                    st.success("✅ Detection Complete! (Demo)")
                    st.info("**Sample Result:**\n- Disease: Early Blight\n- Confidence: 92%\n- Treatment: Fungicide recommended")
    
    with col2:
        st.subheader("Recent Detections")
        diseases = [
            {"_id": "1", "disease": "Leaf Spot", "confidence": 0.85},
            {"_id": "2", "disease": "Rust", "confidence": 0.78},
        ]
        df = pd.DataFrame(diseases)
        st.dataframe(df, use_container_width=True)

# ============================================
# 4. WEATHER ADVISORY PAGE
# ============================================
def weather_page():
    st.title("☀️ Weather Advisory")
    
    col1, col2 = st.columns(2)
    with col1:
        latitude = st.number_input("Latitude", value=20.5937)
    with col2:
        longitude = st.number_input("Longitude", value=78.9629)
    
    if st.button("Get Weather Data", use_container_width=True, type="primary"):
        st.info("📌 **Demo Mode** - Showing sample weather data")
        
        weather_data = {
            "temperature": 28,
            "humidity": 65,
            "windSpeed": 12,
            "rainfall": 2,
        }
        
        st.subheader("📍 Current Weather")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("🌡️ Temperature", f"{weather_data.get('temperature')}°C")
        with col2:
            st.metric("💧 Humidity", f"{weather_data.get('humidity')}%")
        with col3:
            st.metric("💨 Wind Speed", f"{weather_data.get('windSpeed')} km/h")
        with col4:
            st.metric("🌧️ Rainfall", f"{weather_data.get('rainfall')}mm")
        
        st.divider()
        
        st.subheader("🌾 Agricultural Advisory")
        col1, col2 = st.columns(2)
        with col1:
            st.info("💧 **Irrigation**: Water deeply 2-3 times per week")
        with col2:
            st.warning("🧪 **Pesticide**: Spray early morning for better effectiveness")
        
        st.divider()
        
        st.subheader("⚠️ Weather Alerts")
        st.warning("🟡 High temperature expected - Water crops frequently")
        
        st.divider()
        
        st.subheader("📅 10-Day Forecast")
        forecast = []
        for i in range(10):
            forecast.append({
                "date": (datetime.now() + timedelta(days=i)).strftime("%Y-%m-%d"),
                "temp": 28-i%5,
                "condition": "Partly Cloudy"
            })
        forecast_df = pd.DataFrame(forecast)
        st.dataframe(forecast_df, use_container_width=True)

# ============================================
# 5. PRICE PREDICTION PAGE
# ============================================
def price_page():
    st.title("💹 Price Prediction & Analysis")
    
    col1, col2 = st.columns(2)
    with col1:
        crop = st.selectbox("Select Crop", ["Wheat", "Rice", "Corn", "Cotton", "Sugarcane"])
    with col2:
        region = st.selectbox("Select Region", ["North", "South", "East", "West", "Central"])
    
    if st.button("Get Price Analysis", use_container_width=True, type="primary"):
        st.info("📌 **Demo Mode** - Showing sample price data")
        
        prices = {
            "currentPrice": 2500,
            "predictedPrice": 2650,
            "trend": "up",
        }
        
        st.subheader("📊 Price Information")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("💰 Current Price", f"₹{prices.get('currentPrice')}/kg")
        with col2:
            st.metric("📈 Predicted (7d)", f"₹{prices.get('predictedPrice')}/kg")
        with col3:
            trend = prices.get('trend', 'stable')
            st.metric("📊 Trend", "📈 up" if trend == "up" else "📉 down")
        with col4:
            st.metric("💡 Action", "Sell in 3 days")
        
        st.divider()
        
        # Historical chart
        history = []
        for i in range(30):
            history.append({"date": (datetime.now() - timedelta(days=30-i)).strftime("%Y-%m-%d"), "price": 2500 + (i%10)*50})
        
        df = pd.DataFrame(history)
        fig = px.line(df, x='date', y='price', title=f'{crop} Price - Last 30 Days')
        st.plotly_chart(fig, use_container_width=True)

# ============================================
# 6. IoT MONITORING PAGE
# ============================================
def iot_page():
    st.title("🌐 IoT Sensor Monitoring")
    
    st.subheader("📱 Your Devices")
    
    devices = [
        {"_id": "1", "name": "Field 1 Sensor", "location": "North Field"},
        {"_id": "2", "name": "Field 2 Sensor", "location": "South Field"},
    ]
    
    st.info("📌 **Demo Mode** - Showing sample devices")
    
    device_ids = [d.get('_id') for d in devices]
    selected_device = st.selectbox("Select Device", device_ids)
    
    status = {
        "active": True,
        "battery": 85,
        "signal": 90,
        "readings": {
            "soilMoisture": 65,
            "temperature": 28,
            "humidity": 70,
            "pH": 6.5,
            "EC": 1.2,
            "NPK": "N:80 P:40 K:120"
        }
    }
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Status", "🟢 Active")
    with col2:
        st.metric("Battery", f"{status.get('battery')}%")
    with col3:
        st.metric("Signal", f"{status.get('signal')}%")
    
    st.divider()
    
    st.subheader("📊 Real-time Sensor Readings")
    readings = status.get('readings', {})
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("🌱 Soil Moisture", f"{readings.get('soilMoisture')}%")
        st.metric("🌡️ Temperature", f"{readings.get('temperature')}°C")
    with col2:
        st.metric("💧 Humidity", f"{readings.get('humidity')}%")
        st.metric("🧪 pH Level", f"{readings.get('pH')}")
    with col3:
        st.metric("⚡ EC", f"{readings.get('EC')} mS/cm")
        st.metric("🌾 NPK", readings.get('NPK', 'N/A'))

# ============================================
# 7. CHATBOT PAGE
# ============================================
def chatbot_page():
    st.title("💬 AI Farming Assistant")
    
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    
    # Display chat messages
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.write(message["content"])
    
    # Chat input
    user_input = st.chat_input("Ask about farming, weather, diseases, prices...")
    
    if user_input:
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        
        # Demo responses
        if "weather" in user_input.lower():
            ai_response = "☀️ The weather looks good for planting. Make sure to water adequately."
        elif "disease" in user_input.lower():
            ai_response = "🦠 Early blight is common in wet conditions. Use fungicide and improve drainage."
        elif "price" in user_input.lower():
            ai_response = "💹 Wheat prices are expected to rise in the next week. Good time to plan."
        else:
            ai_response = "🤖 That's a great farming question! I'd recommend consulting local agriculture experts."
        
        st.session_state.chat_history.append({"role": "assistant", "content": ai_response})
        st.rerun()

# ============================================
# 8. ACCOUNT SETTINGS PAGE
# ============================================
def settings_page():
    st.title("⚙️ Account Settings")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("👤 Profile Information")
        user = st.session_state.user
        st.write(f"**Name**: {user.get('name', 'N/A')}")
        st.write(f"**Email**: {user.get('email', 'N/A')}")
        st.write(f"**Phone**: {user.get('phone', 'N/A')}")
    
    with col2:
        st.subheader("🔄 Update Profile")
        new_name = st.text_input("Name", user.get('name', ''))
        new_phone = st.text_input("Phone", user.get('phone', ''))
        
        if st.button("Save Changes", use_container_width=True):
            st.success("✅ Profile updated! (Demo Mode)")

# ============================================
# MAIN APP
# ============================================
def main():
    if not st.session_state.logged_in:
        login_page()
    else:
        # Sidebar Navigation
        st.sidebar.title(f"👋 {st.session_state.user.get('name', 'Farmer')}")
        st.sidebar.divider()
        
        page = st.sidebar.radio(
            "Navigation",
            [
                "📊 Dashboard",
                "🦠 Disease Detection",
                "☀️ Weather",
                "💹 Price Analysis",
                "🌐 IoT Monitoring",
                "💬 AI Assistant",
                "⚙️ Settings"
            ]
        )
        
        st.sidebar.divider()
        
        col1, col2 = st.sidebar.columns(2)
        with col1:
            if st.button("🔄 Refresh", use_container_width=True):
                st.rerun()
        with col2:
            if st.button("🚪 Logout", use_container_width=True):
                st.session_state.logged_in = False
                st.session_state.user = None
                st.session_state.token = None
                st.rerun()
        
        # Page Routing
        if page == "📊 Dashboard":
            dashboard_page()
        elif page == "🦠 Disease Detection":
            disease_detection_page()
        elif page == "☀️ Weather":
            weather_page()
        elif page == "💹 Price Analysis":
            price_page()
        elif page == "🌐 IoT Monitoring":
            iot_page()
        elif page == "💬 AI Assistant":
            chatbot_page()
        elif page == "⚙️ Settings":
            settings_page()

if __name__ == "__main__":
    main()
