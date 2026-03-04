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
    .success-box {
        background-color: #d4edda;
        padding: 15px;
        border-radius: 5px;
        color: #155724;
        border-left: 4px solid #28a745;
    }
    .warning-box {
        background-color: #fff3cd;
        padding: 15px;
        border-radius: 5px;
        color: #856404;
        border-left: 4px solid #ffc107;
    }
    .danger-box {
        background-color: #f8d7da;
        padding: 15px;
        border-radius: 5px;
        color: #721c24;
        border-left: 4px solid #dc3545;
    }
    </style>
    """, unsafe_allow_html=True)

# API Configuration
API_URL = "http://localhost:5000/api"  # Change this for cloud deployment

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
            if st.button("🔴 DEMO MODE", use_container_width=True):
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
                st.error("❌ Backend not running!\n\n**To enable registration:**\n```bash\ncd backend\nnpm install\nnpm start\n```\n\nFor now, you can explore the UI!")
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
        response = requests.get(f"{API_URL}/crops/metrics", headers=headers, timeout=10)
        if response.status_code == 200:
            metrics = response.json()
        else:
            metrics = None
    except requests.exceptions.ConnectionError:
        metrics = None
    
    # Show mock data if backend is down
    if metrics is None:
        if st.session_state.token != "demo_token":
            st.error("❌ Backend connection failed. Please start the backend:\n```bash\ncd backend\nnpm start\n```")
            return
        
        # Demo data
        st.info("📌 **Demo Mode** - Showing sample data. Start backend for real data!")
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
            if st.session_state.token == "demo_token":
                # Mock crops for demo
                crops = [
                    {"_id": "1", "name": "Rice", "type": "Rice", "area": 2.5, "status": "Growing"},
                    {"_id": "2", "name": "Wheat", "type": "Wheat", "area": 3.0, "status": "Germination"},
                    {"_id": "3", "name": "Cotton", "type": "Cotton", "area": 1.5, "status": "Growing"},
                ]
                st.dataframe(pd.DataFrame(crops), use_container_width=True)
            else:
                st.warning("No crops added yet. Add your first crop!")
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
                except requests.exceptions.ConnectionError:
                    st.success("✅ Crop added! (Demo Mode - data stored locally)")
                except Exception as e:
                    st.error(f"Error: {str(e)}")
    
    with tab3:
        st.subheader("Crop Analytics")
        # Generate sample chart
        chart_data = pd.DataFrame({
            "Date": pd.date_range(start="2024-01-01", periods=30),
            "Growth": range(30, 60)
        })
        fig = px.line(chart_data, x="Date", y="Growth", title="Crop Growth Progress")
        st.plotly_chart(fig, use_container_width=True)

# ============================================
# 3. DISEASE DETECTION PAGE
# ============================================
def disease_detection_page():
    st.title("🦠 Disease Detection (AI)")
    
    headers = {"Authorization": f"Bearer {st.session_state.token}"}
    
    # Check backend
    try:
        requests.get(f"{API_URL}/crops", headers=headers, timeout=2)
        backend_ok = True
    except:
        backend_ok = False
    
    if not backend_ok and st.session_state.token != "demo_token":
        st.error("❌ Backend connection failed. Start backend to use disease detection.")
        return
    
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
                crops = [{"_id": "1", "name": "Rice"}, {"_id": "2", "name": "Wheat"}]  # Demo crops
            
            crop_ids = [c.get("_id", c.get("id")) for c in crops]
            
            if crop_ids:
                selected_crop = st.selectbox("Select Crop", crop_ids)
                
                if st.button("🔍 Detect Disease", use_container_width=True, type="primary"):
                    if backend_ok:
                        # Real detection
                        img_bytes = io.BytesIO()
                        image.save(img_bytes, format="PNG")
                        img_bytes.seek(0)
                        
                        files = {'image': ('upload.png', img_bytes, 'image/png')}
                        
                        try:
                            detect_response = requests.post(
                                f"{API_URL}/diseases/detect/{selected_crop}",
                                files=files,
                                headers=headers,
                                timeout=30
                            )
                            
                            if detect_response.status_code == 200:
                                result = detect_response.json()
                                st.success(f"✅ Detection Complete!")
                                st.write(result)
                            else:
                                st.error("Detection failed")
                        except Exception as e:
                            st.error(f"Error: {str(e)}")
                    else:
                        # Demo mode
                        st.success("✅ Detection Complete! (Demo)")
                        st.info("""
                        **Sample Result:**
                        - Disease: Early Blight
                        - Confidence: 92%
                        - Severity: Moderate
                        - Treatment: Fungicide recommended
                        """)
    
    with col2:
        st.subheader("Recent Detections")
        try:
            diseases_response = requests.get(f"{API_URL}/diseases", headers=headers, timeout=10)
            if diseases_response.status_code == 200:
                diseases = diseases_response.json()
            else:
                diseases = None
        except:
            diseases = None
        
        if diseases is None:
            if st.session_state.token == "demo_token":
                # Demo data
                diseases = [
                    {"_id": "1", "cropId": "1", "disease": "Leaf Spot", "confidence": 0.85},
                    {"_id": "2", "cropId": "2", "disease": "Rust", "confidence": 0.78},
                ]
                df = pd.DataFrame(diseases)
                st.dataframe(df, use_container_width=True)
            else:
                st.info("No disease records yet")
        else:
            if diseases:
                df = pd.DataFrame(diseases[:10])
                st.dataframe(df, use_container_width=True)
            else:
                st.info("No disease records yet")

# ============================================
# 4. WEATHER ADVISORY PAGE
# ============================================
def weather_page():
    st.title("☀️ Weather Advisory")
    
    headers = {"Authorization": f"Bearer {st.session_state.token}"}
    
    col1, col2 = st.columns(2)
    
    with col1:
        latitude = st.number_input("Latitude", value=20.5937)
    with col2:
        longitude = st.number_input("Longitude", value=78.9629)
    
    if st.button("Get Weather Data", use_container_width=True, type="primary"):
        try:
            weather_response = requests.get(
                f"{API_URL}/weather/data",
                params={"latitude": latitude, "longitude": longitude},
                headers=headers,
                timeout=10
            )
            
            if weather_response.status_code == 200:
                weather_data = weather_response.json()
            else:
                weather_data = None
        except:
            weather_data = None
        
        # Demo data if backend is down
        if weather_data is None:
            weather_data = {
                "temperature": 28,
                "humidity": 65,
                "windSpeed": 12,
                "rainfall": 2,
                "advisory": {"irrigation": "Water deeply", "pesticide": "Spray early morning"},
                "alerts": [{"severity": "medium", "description": "High temperature expected"}]
            }
            st.info("📌 **Demo Mode** - Showing sample weather data")
        
        # Current Weather
        st.subheader("📍 Current Weather")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("🌡️ Temperature", f"{weather_data.get('temperature', 0)}°C")
        with col2:
            st.metric("💧 Humidity", f"{weather_data.get('humidity', 0)}%")
        with col3:
            st.metric("💨 Wind Speed", f"{weather_data.get('windSpeed', 0)} km/h")
        with col4:
            st.metric("🌧️ Rainfall", f"{weather_data.get('rainfall', 0)}mm")
        
        # Advisory
        st.divider()
        st.subheader("🌾 Agricultural Advisory")
        advisory = weather_data.get('advisory', {})
        if advisory:
            col1, col2 = st.columns(2)
            with col1:
                st.info(f"💧 **Irrigation**: {advisory.get('irrigation', 'N/A')}")
            with col2:
                st.warning(f"🧪 **Pesticide**: {advisory.get('pesticide', 'N/A')}")
        
        # Alerts
        st.divider()
        alerts = weather_data.get('alerts', [])
        if alerts:
            st.subheader("⚠️ Weather Alerts")
            for alert in alerts:
                severity = alert.get('severity', 'info')
                if severity == 'high':
                    st.error(f"🔴 {alert.get('description', 'Alert')}")
                elif severity == 'medium':
                    st.warning(f"🟡 {alert.get('description', 'Alert')}")
                else:
                    st.info(f"🔵 {alert.get('description', 'Alert')}")
        
        # Forecast
        st.divider()
        try:
            forecast_response = requests.get(
                f"{API_URL}/weather/forecast",
                params={"latitude": latitude, "longitude": longitude},
                headers=headers,
                timeout=10
            )
            forecast = forecast_response.json() if forecast_response.status_code == 200 else None
        except:
            forecast = None
        
        if forecast is None:
            # Demo forecast
            forecast = []
            for i in range(10):
                forecast.append({"date": (datetime.now() + timedelta(days=i)).strftime("%Y-%m-%d"), "temp": 28-i%5, "condition": "Partly Cloudy"})
        
        st.subheader("📅 10-Day Forecast")
        if isinstance(forecast, list) and forecast:
            forecast_df = pd.DataFrame(forecast[:10])
            st.dataframe(forecast_df, use_container_width=True)

# ============================================
# 5. PRICE PREDICTION PAGE
# ============================================
def price_page():
    st.title("💹 Price Prediction & Analysis")
    
    try:
        headers = {"Authorization": f"Bearer {st.session_state.token}"}
        
        col1, col2 = st.columns(2)
        with col1:
            crop = st.selectbox("Select Crop", ["Wheat", "Rice", "Corn", "Cotton", "Sugarcane"])
        with col2:
            region = st.selectbox("Select Region", ["North", "South", "East", "West", "Central"])
        
        if st.button("Get Price Analysis", use_container_width=True, type="primary"):
            try:
                response = requests.get(
                    f"{API_URL}/prices/prediction",
                    params={"crop": crop, "region": region},
                    headers=headers,
                    timeout=10
                )
                
                if response.status_code == 200:
                    prices = response.json()
                    
                    # Price Metrics
                    st.subheader("📊 Price Information")
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric("💰 Current Price", f"₹{prices.get('currentPrice', 0)}/kg")
                    with col2:
                        st.metric("📈 Predicted Price (7d)", f"₹{prices.get('predictedPrice', 0)}/kg")
                    with col3:
                        trend = prices.get('trend', 'stable')
                        st.metric("📊 Trend", f"{'📈' if trend == 'up' else '📉' if trend == 'down' else '➡️'} {trend}")
                    with col4:
                        st.metric("💡 Action", prices.get('recommendation', 'Hold'))
                    
                    # Historical Data
                    st.divider()
                    history_response = requests.get(
                        f"{API_URL}/prices/history",
                        params={"crop": crop, "days": 30},
                        headers=headers,
                        timeout=10
                    )
                    
                    if history_response.status_code == 200:
                        history = history_response.json()
                        if isinstance(history, list):
                            df = pd.DataFrame(history)
                            if 'date' in df.columns and 'price' in df.columns:
                                fig = px.line(df, x='date', y='price', title=f'{crop} Price - Last 30 Days')
                                st.plotly_chart(fig, use_container_width=True)
                    
                    # Market Insights
                    st.divider()
                    insights_response = requests.get(
                        f"{API_URL}/prices/insights",
                        params={"crop": crop},
                        headers=headers,
                        timeout=10
                    )
                    
                    if insights_response.status_code == 200:
                        insights = insights_response.json()
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.info(f"📊 Avg: ₹{insights.get('averagePrice', 0)}/kg")
                        with col2:
                            st.warning(f"⬆️ Max: ₹{insights.get('maxPrice', 0)}/kg")
                        with col3:
                            st.error(f"⬇️ Min: ₹{insights.get('minPrice', 0)}/kg")
                
            except Exception as e:
                st.error(f"Error: {str(e)}")
    
    except Exception as e:
        st.error(f"Error: {str(e)}")

# ============================================
# 6. IoT MONITORING PAGE
# ============================================
def iot_page():
    st.title("🌐 IoT Sensor Monitoring")
    
    try:
        headers = {"Authorization": f"Bearer {st.session_state.token}"}
        
        # Device List
        st.subheader("📱 Your Devices")
        devices_response = requests.get(f"{API_URL}/iot/devices", headers=headers, timeout=10)
        
        if devices_response.status_code == 200:
            devices = devices_response.json()
            
            if devices:
                device_ids = [d.get('_id', d.get('id')) for d in devices]
                selected_device = st.selectbox("Select Device", device_ids)
                
                # Device Status
                status_response = requests.get(
                    f"{API_URL}/iot/{selected_device}/status",
                    headers=headers,
                    timeout=10
                )
                
                if status_response.status_code == 200:
                    status = status_response.json()
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        device_status = "🟢 Active" if status.get('active') else "🔴 Inactive"
                        st.metric("Status", device_status)
                    with col2:
                        st.metric("Battery", f"{status.get('battery', 0)}%")
                    with col3:
                        st.metric("Signal", f"{status.get('signal', 0)}%")
                    
                    # Real-time Readings
                    st.divider()
                    st.subheader("📊 Real-time Sensor Readings")
                    
                    readings = status.get('readings', {})
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("🌱 Soil Moisture", f"{readings.get('soilMoisture', 0)}%")
                        st.metric("🌡️ Temperature", f"{readings.get('temperature', 0)}°C")
                    with col2:
                        st.metric("💧 Humidity", f"{readings.get('humidity', 0)}%")
                        st.metric("🧪 pH Level", f"{readings.get('pH', 0)}")
                    with col3:
                        st.metric("⚡ EC", f"{readings.get('EC', 0)} mS/cm")
                        st.metric("🌾 NPK", readings.get('NPK', 'N/A'))
                    
                    # Historical Data
                    st.divider()
                    st.subheader("📈 Historical Data")
                    history_response = requests.get(
                        f"{API_URL}/iot/{selected_device}/history",
                        params={"days": 7},
                        headers=headers,
                        timeout=10
                    )
                    
                    if history_response.status_code == 200:
                        history = history_response.json()
                        if isinstance(history, list):
                            df = pd.DataFrame(history)
                            st.dataframe(df, use_container_width=True)
                    
                    # Alerts
                    st.divider()
                    alerts_response = requests.get(
                        f"{API_URL}/iot/{selected_device}/alerts",
                        headers=headers,
                        timeout=10
                    )
                    
                    if alerts_response.status_code == 200:
                        alerts = alerts_response.json()
                        if alerts:
                            st.subheader("⚠️ Sensor Alerts")
                            for alert in alerts[:10]:
                                severity = alert.get('severity', 'info')
                                if severity == 'high':
                                    st.error(f"🔴 {alert.get('message', 'Alert')}")
                                elif severity == 'medium':
                                    st.warning(f"🟡 {alert.get('message', 'Alert')}")
                                else:
                                    st.info(f"🔵 {alert.get('message', 'Alert')}")
            else:
                st.info("No devices connected. Register a device first!")
    
    except Exception as e:
        st.error(f"Error: {str(e)}")

# ============================================
# 7. CHATBOT PAGE
# ============================================
def chatbot_page():
    st.title("💬 AI Farming Assistant")
    
    try:
        headers = {"Authorization": f"Bearer {st.session_state.token}"}
        
        # Chat History
        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []
        
        # Display chat messages
        for message in st.session_state.chat_history:
            with st.chat_message(message["role"]):
                st.write(message["content"])
        
        # Chat input
        user_input = st.chat_input("Ask about farming, weather, diseases, prices...")
        
        if user_input:
            # Add user message
            st.session_state.chat_history.append({"role": "user", "content": user_input})
            
            try:
                # Get AI response
                response = requests.post(
                    f"{API_URL}/chatbot/query",
                    json={"message": user_input},
                    headers=headers,
                    timeout=30
                )
                
                if response.status_code == 200:
                    ai_response = response.json().get("reply", "Sorry, I couldn't understand.")
                else:
                    ai_response = "Error getting response from AI."
                
                # Add AI message
                st.session_state.chat_history.append({"role": "assistant", "content": ai_response})
                st.rerun()
            
            except Exception as e:
                st.error(f"Error: {str(e)}")
    
    except Exception as e:
        st.error(f"Error: {str(e)}")

# ============================================
# 8. ACCOUNT SETTINGS PAGE
# ============================================
def settings_page():
    st.title("⚙️ Account Settings")
    
    try:
        headers = {"Authorization": f"Bearer {st.session_state.token}"}
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("👤 Profile Information")
            st.write(f"**Name**: {st.session_state.user.get('name', 'N/A')}")
            st.write(f"**Email**: {st.session_state.user.get('email', 'N/A')}")
            st.write(f"**Phone**: {st.session_state.user.get('phone', 'N/A')}")
        
        with col2:
            st.subheader("🔄 Update Profile")
            new_name = st.text_input("Name", st.session_state.user.get('name', ''))
            new_phone = st.text_input("Phone", st.session_state.user.get('phone', ''))
            
            if st.button("Save Changes", use_container_width=True):
                try:
                    update_response = requests.put(
                        f"{API_URL}/user/profile",
                        json={"name": new_name, "phone": new_phone},
                        headers=headers,
                        timeout=10
                    )
                    if update_response.status_code == 200:
                        st.success("✅ Profile updated!")
                        st.session_state.user = update_response.json()
                    else:
                        st.error("Failed to update profile")
                except Exception as e:
                    st.error(f"Error: {str(e)}")
        
        st.divider()
        
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("🔐 Password")
            old_pass = st.text_input("Current Password", type="password")
            new_pass = st.text_input("New Password", type="password")
            
            if st.button("Change Password", use_container_width=True):
                try:
                    pass_response = requests.post(
                        f"{API_URL}/auth/change-password",
                        json={"oldPassword": old_pass, "newPassword": new_pass},
                        headers=headers,
                        timeout=10
                    )
                    if pass_response.status_code == 200:
                        st.success("✅ Password changed!")
                    else:
                        st.error("Failed to change password")
                except Exception as e:
                    st.error(f"Error: {str(e)}")
        
        with col2:
            st.subheader("⚠️ Danger Zone")
            if st.button("🔴 Delete Account", use_container_width=True):
                with st.form("delete_account"):
                    confirm = st.checkbox("I understand this action is permanent")
                    if st.form_submit_button("Confirm Delete"):
                        try:
                            delete_response = requests.delete(
                                f"{API_URL}/user/account",
                                headers=headers,
                                timeout=10
                            )
                            if delete_response.status_code == 200:
                                st.success("Account deleted")
                                st.session_state.logged_in = False
                                st.rerun()
                            else:
                                st.error("Failed to delete account")
                        except Exception as e:
                            st.error(f"Error: {str(e)}")
    
    except Exception as e:
        st.error(f"Error: {str(e)}")

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
