import streamlit as st
import pandas as pd
import numpy as np
import os
import pickle
import datetime
import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

st.set_page_config(
    page_title="SlumSafe AI",
    page_icon="🚨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- State Initialization ---
if 'prediction_made' not in st.session_state:
    st.session_state.prediction_made = False
if 'risk_level' not in st.session_state:
    st.session_state.risk_level = 0
if 'report_success' not in st.session_state:
    st.session_state.report_success = False

# --- Geolocation via JS Eval ---
from streamlit_js_eval import streamlit_js_eval, get_geolocation
# This calls the browser's native Geolocation API in a non-sandboxed way
loc = get_geolocation()

# --- Load Emergency Contacts ---
EMERGENCY_DATA_FILE = os.path.join(BASE_DIR, "data", "emergency_contacts.csv")
def get_nearest_responder(u_lat, u_lon):
    if not os.path.exists(EMERGENCY_DATA_FILE):
        return None
    try:
        e_df = pd.read_csv(EMERGENCY_DATA_FILE)
        # Use Euclidean distance for simplicity
        e_df['dist'] = np.sqrt((e_df['latitude'] - u_lat)**2 + (e_df['longitude'] - u_lon)**2)
        return e_df.sort_values('dist').iloc[0]
    except Exception:
        return None



# --- Custom CSS for Premium Design Aesthetics ---
st.markdown("""
    <style>
        /* Import Google Font */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');

        /* Base Typography */
        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif !important;
        }

        /* Dark blue/black gradient background */
        [data-testid="stAppViewContainer"] {
            background: linear-gradient(135deg, #050b14 0%, #0d172e 100%);
            color: #f0f4f8;
        }
        
        /* Glassmorphism Sidebar */
        [data-testid="stSidebar"] > div:first-child {
            background: linear-gradient(180deg, rgba(6, 11, 20, 0.95) 0%, rgba(13, 22, 40, 0.95) 100%);
            backdrop-filter: blur(15px);
            border-right: 1px solid rgba(255, 255, 255, 0.05);
            box-shadow: 4px 0 25px rgba(0, 0, 0, 0.6);
        }

        /* Main Container Spacing */
        .block-container {
            padding-top: 3rem;
            padding-bottom: 3rem;
            max-width: 1200px;
        }

        /* Beautiful Buttons with hover micro-animations */
        div.stButton > button:first-child {
            width: 100%;
            background: linear-gradient(90deg, #0d6efd, #0043a8);
            color: white;
            font-weight: 600;
            border-radius: 12px;
            border: 1px solid rgba(255,255,255,0.1);
            padding: 0.6rem 1rem;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(13, 110, 253, 0.3);
        }

        div.stButton > button:first-child:hover {
            transform: translateY(-3px);
            box-shadow: 0 8px 25px rgba(13, 110, 253, 0.5);
            color: #ffffff;
            border: 1px solid rgba(255,255,255,0.3);
        }
        
        /* Input Fields Configuration */
        .stNumberInput > div > div > input, .stTextInput > div > div > input, .stSelectbox > div > div > div {
            background-color: rgba(255, 255, 255, 0.03) !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            border-radius: 8px !important;
            color: #ffffff !important;
        }
        
        /* Rounded Map Frame container effect */
        iframe {
            border-radius: 16px;
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.5);
            border: 1px solid rgba(255, 255, 255, 0.05);
        }
        
        /* Custom Custom Divider */
        hr {
            border-color: rgba(255, 255, 255, 0.08);
            margin: 2rem 0;
            border-width: 1px;
        }
    </style>
""", unsafe_allow_html=True)

# --- Main App Header ---
st.markdown("""
<div style="text-align: center; margin-bottom: 2.5rem;">
    <h1 style="font-weight: 800; color: #ffffff; text-shadow: 0 4px 20px rgba(0,0,0,0.5); display: inline-block;">
        🚨 SlumSafe AI
    </h1>
</div>
""", unsafe_allow_html=True)

# --- Sidebar Content ---
with st.sidebar:
    st.markdown("<h3 style='color: #ffffff; font-weight: 600; margin-bottom: 1.5rem;'>Crime Risk Prediction</h3>", unsafe_allow_html=True)
    
    # Region Selection
    city = st.selectbox("Quick Jump to Region", ["Mumbai (Dharavi)", "Goa", "Bangalore", "Custom (Chicago / Other)"])
    if city == "Mumbai (Dharavi)":
        default_lat, default_lon = 19.0380, 72.8538
    elif city == "Goa":
        default_lat, default_lon = 15.4909, 73.8278
    elif city == "Bangalore":
        default_lat, default_lon = 12.9716, 77.5946
    else:
        default_lat, default_lon = 41.8781, -87.6298

    # Input fields
    lat = st.number_input("Latitude", value=default_lat, format="%.4f")
    lon = st.number_input("Longitude", value=default_lon, format="%.4f")
    
    # Hour slider
    st.markdown("<div style='margin-top: 1rem;'></div>", unsafe_allow_html=True)
    hour = st.slider("Select Hour", min_value=0, max_value=23, value=22, format="%d", help="Select time in 24-hr format")
    
    # Predict button
    st.markdown("<div style='margin-top: 1.5rem; margin-bottom: 1.5rem;'></div>", unsafe_allow_html=True)
    predict_clicked = st.button("Predict Risk", key="predict_btn")
    
    # --- ML Model Integration ---
    if predict_clicked:
        st.session_state.prediction_made = True
        
        # Load the model from model/model.pkl dynamically resolving parent directory
        model_path = os.path.join(BASE_DIR, "model", "model.pkl")
        if os.path.exists(model_path):
            try:
                with open(model_path, 'rb') as f:
                    model = pickle.load(f)
                
                # Make prediction based on Latitude, Longitude, and Hour
                # Using a DataFrame with feature names to match training format and prevent warnings
                input_df = pd.DataFrame([[lat, lon, hour]], columns=['latitude', 'longitude', 'hour'])
                prediction = model.predict(input_df)
                
                # model logic: 2 is High, 1 is Medium, 0 is Low
                st.session_state.risk_level = int(prediction[0])
            except Exception as e:
                st.sidebar.error(f"Error executing model: {e}")
                st.session_state.risk_level = 2 if ((hour >= 20) or (hour <= 4)) else (1 if 18 <= hour <= 21 else 0)
        else:
            st.session_state.risk_level = 2 if ((hour >= 20) or (hour <= 4)) else (1 if 18 <= hour <= 21 else 0)

    # Sync variable for display logic below
    risk_level = st.session_state.risk_level
    is_high_risk = (risk_level >= 1) # Keep legacy flag mapping for Heatmap
    
    # Render Colored Result Box dynamically based on the prediction
    if st.session_state.prediction_made:
        if risk_level == 2:
            st.markdown("""
            <div style="background: linear-gradient(135deg, rgba(220, 53, 69, 0.9), rgba(150, 20, 40, 0.8)); 
                        color: white; border-radius: 12px; padding: 18px; text-align: center; 
                        box-shadow: 0 8px 25px rgba(220, 53, 69, 0.4); border: 1px solid rgba(255, 100, 100, 0.2); 
                        margin-bottom: 1rem; transition: transform 0.3s ease;">
                <h4 style='margin:0 0 5px 0; font-weight: 800; text-transform: uppercase; font-size: 1.05rem; letter-spacing: 1px;'>⚠️ High Risk Area Detected</h4>
            </div>
            """, unsafe_allow_html=True)
        elif risk_level == 1:
            st.markdown("""
            <div style="background: linear-gradient(135deg, rgba(255, 193, 7, 0.9), rgba(200, 140, 0, 0.8)); 
                        color: white; border-radius: 12px; padding: 18px; text-align: center; 
                        box-shadow: 0 8px 25px rgba(255, 193, 7, 0.4); border: 1px solid rgba(255, 200, 50, 0.2); 
                        margin-bottom: 1rem; transition: transform 0.3s ease;">
                <h4 style='margin:0 0 5px 0; font-weight: 800; text-transform: uppercase; font-size: 1.05rem; letter-spacing: 1px;'>⚠️ Medium Risk Area</h4>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="background: linear-gradient(135deg, rgba(25, 135, 84, 0.9), rgba(15, 90, 50, 0.8)); 
                        color: white; border-radius: 12px; padding: 18px; text-align: center; 
                        box-shadow: 0 8px 25px rgba(25, 135, 84, 0.4); border: 1px solid rgba(100, 255, 150, 0.2); 
                        margin-bottom: 1rem; transition: transform 0.3s ease;">
                <h4 style='margin:0 0 5px 0; font-weight: 800; text-transform: uppercase; font-size: 1.05rem; letter-spacing: 1px;'>✅ Low Risk Area Detected</h4>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("<hr>", unsafe_allow_html=True)
    
    # Anonymous Crime Reporting Section
    st.markdown("<h3 style='color: #ffffff; font-weight: 600; margin-bottom: 0.5rem;'>🚨 Report an Incident</h3>", unsafe_allow_html=True)
    
    if st.session_state.get('report_success'):
        st.success("✅ Report securely submitted with live GPS!")
        st.session_state.report_success = False
        
    st.markdown("<p style='color: #a0aec0; font-size: 0.85em; margin-bottom: 1rem;'>1-Tap Community Reporting (Live GPS)</p>", unsafe_allow_html=True)
    
    # Check if location is available
    report_lat, report_lon = 12.9716, 77.5946 # Defaults
    if loc and 'coords' in loc:
        report_lat = loc['coords']['latitude']
        report_lon = loc['coords']['longitude']
        st.markdown(f"<p style='color: #51cf66; font-size: 0.85em; margin-bottom: 1rem;'>📍 Live GPS Active: {report_lat:.4f}, {report_lon:.4f}</p>", unsafe_allow_html=True)
    else:
        st.markdown("<p style='color: #ffc107; font-size: 0.85em; margin-bottom: 1rem;'>⌛ Waiting for GPS permission...</p>", unsafe_allow_html=True)

    def save_report(crime_type):
        data_dir = os.path.join(BASE_DIR, "data")
        reports_file = os.path.join(data_dir, "reports.csv")
        os.makedirs(data_dir, exist_ok=True)
        
        new_report = pd.DataFrame([{
            "crime_type": crime_type,
            "latitude": report_lat,
            "longitude": report_lon,
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }])
        
        if not os.path.exists(reports_file):
            new_report.to_csv(reports_file, index=False)
        else:
            new_report.to_csv(reports_file, mode='a', header=False, index=False)
        st.session_state.report_success = True
            
    col1, col2, col3 = st.columns(3)
    if col1.button("👜 Theft", use_container_width=True, key="btn_theft"):
        save_report("Theft")
        st.rerun()
    if col2.button("⚠️ Violence", use_container_width=True, key="btn_violence"):
        save_report("Violence")
        st.rerun()
    if col3.button("💊 Drug", use_container_width=True, key="btn_drug"):
        save_report("Drug Activity")
        st.rerun()

    # Display: recent reports list
    reports_file = os.path.join(BASE_DIR, "data", "reports.csv")
    if os.path.exists(reports_file):
        st.markdown("<h4 style='color: #ffffff; font-weight: 600; margin-top: 1.5rem; font-size: 1rem;'>Recent Community Reports</h4>", unsafe_allow_html=True)
        try:
            reports_df = pd.read_csv(reports_file)
            # Display last 5 reports (latest first)
            recent = reports_df.tail(5).iloc[::-1]
            for _, r in recent.iterrows():
                try:
                    lat_disp = float(r.get('latitude', 12.9716))
                    lon_disp = float(r.get('longitude', 77.5946))
                except:
                    lat_disp, lon_disp = 12.9716, 77.5946
                    
                st.markdown(f"""
                <div style="background-color: rgba(255, 255, 255, 0.03); color: #e2e8f0; border-radius: 8px; 
                            padding: 10px; margin-bottom: 8px; border: 1px solid rgba(255, 255, 255, 0.05);
                            box-shadow: 0 2px 5px rgba(0,0,0,0.2);">
                    <div style='font-size: 0.75em; color: #a0aec0; margin-bottom: 3px;'>{r.get('timestamp', 'Unknown Time')}</div>
                    <div style='font-size: 0.9em;'>🚨 <b>{r.get('crime_type', 'Unknown')}</b> reported at ({lat_disp:.4f}, {lon_disp:.4f})</div>
                </div>
                """, unsafe_allow_html=True)
        except Exception:
             pass
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("<h3 style='color: #ff6b6b; font-weight: 600; margin-bottom: 1rem;'>Emergency Action</h3>", unsafe_allow_html=True)
    emergency_clicked = st.button("🚨 Emergency Help", key="emergency_btn")
    if emergency_clicked:
        st.error("Calling emergency contact...")
        st.markdown("<div style='text-align: center; margin-top: 10px;'><a href='tel:+91XXXXXXXXXX' style='color: #ff6b6b; font-weight: bold; font-size: 1.2rem; text-decoration: none;'>📞 +91XXXXXXXXXX</a></div>", unsafe_allow_html=True)
        
# --- Main Panel Content ---

# Alert Banner and Recommended Actions logic
if st.session_state.prediction_made:
    if risk_level == 2:
        banner_html = """
        <div style="background: rgba(220, 53, 69, 0.15); border-left: 6px solid #dc3545; padding: 1.25rem 1.5rem; 
                    border-radius: 12px; box-shadow: 0 8px 30px rgba(0,0,0,0.2); margin-bottom: 1rem;
                    backdrop-filter: blur(10px); border: 1px solid rgba(255,255,255,0.05);">
            <div style="display: flex; align-items: center;">
                <span style="font-size: 2rem; margin-right: 20px;">🚨</span>
                <div>
                    <h4 style="color: #ff6b6b; margin: 0 0 5px 0; font-weight: 800; font-size: 1.2rem;">Danger Zone: High Risk</h4>
                    <p style="color: #f0f4f8; margin: 0; font-size: 1.05rem; opacity: 0.9;">Urgent action required.</p>
                </div>
            </div>
        </div>"""
        action_html = """
        <div style="background: rgba(220, 53, 69, 0.05); border-left: 4px solid #dc3545; padding: 1rem 1.5rem; 
                    border-radius: 8px; margin-bottom: 2.5rem; border: 1px solid rgba(220, 53, 69, 0.3);">
            <h4 style="color: #ff6b6b; margin: 0 0 10px 0;">📋 Recommended Actions</h4>
            <ul style="color: #f0f4f8; margin: 0; padding-left: 20px; line-height: 1.6;">
                <li>Increase police patrolling immediately</li>
                <li>Deploy rapid response teams to the area</li>
                <li>Activate emergency contact alerts for residents</li>
            </ul>
        </div>"""
    elif risk_level == 1:
        banner_html = """
        <div style="background: rgba(255, 193, 7, 0.15); border-left: 6px solid #ffc107; padding: 1.25rem 1.5rem; 
                    border-radius: 12px; box-shadow: 0 8px 30px rgba(0,0,0,0.2); margin-bottom: 1rem;
                    backdrop-filter: blur(10px); border: 1px solid rgba(255,255,255,0.05);">
            <div style="display: flex; align-items: center;">
                <span style="font-size: 2rem; margin-right: 20px;">⚠️</span>
                <div>
                    <h4 style="color: #ffc107; margin: 0 0 5px 0; font-weight: 800; font-size: 1.2rem;">Warning Zone: Medium Risk</h4>
                    <p style="color: #f0f4f8; margin: 0; font-size: 1.05rem; opacity: 0.9;">Preventive action recommended.</p>
                </div>
            </div>
        </div>"""
        action_html = """
        <div style="background: rgba(255, 193, 7, 0.05); border-left: 4px solid #ffc107; padding: 1rem 1.5rem; 
                    border-radius: 8px; margin-bottom: 2.5rem; border: 1px solid rgba(255, 193, 7, 0.3);">
            <h4 style="color: #ffc107; margin: 0 0 10px 0;">📋 Recommended Actions</h4>
            <ul style="color: #f0f4f8; margin: 0; padding-left: 20px; line-height: 1.6;">
                <li>Increase monitoring of key hotspots</li>
                <li>Conduct community awareness programs</li>
                <li>Improve local infrastructure (e.g., street lighting)</li>
            </ul>
        </div>"""
    else:
        banner_html = """
        <div style="background: rgba(25, 135, 84, 0.15); border-left: 6px solid #198754; padding: 1.25rem 1.5rem; 
                    border-radius: 12px; box-shadow: 0 8px 30px rgba(0,0,0,0.2); margin-bottom: 1rem;
                    backdrop-filter: blur(10px); border: 1px solid rgba(255,255,255,0.05);">
            <div style="display: flex; align-items: center;">
                <span style="font-size: 2rem; margin-right: 20px;">🛡️</span>
                <div>
                    <h4 style="color: #51cf66; margin: 0 0 5px 0; font-weight: 800; font-size: 1.2rem;">Safe Zone: Low Risk</h4>
                    <p style="color: #f0f4f8; margin: 0; font-size: 1.05rem; opacity: 0.9;">Routine monitoring.</p>
                </div>
            </div>
        </div>"""
        action_html = """
        <div style="background: rgba(25, 135, 84, 0.05); border-left: 4px solid #198754; padding: 1rem 1.5rem; 
                    border-radius: 8px; margin-bottom: 2.5rem; border: 1px solid rgba(25, 135, 84, 0.3);">
            <h4 style="color: #51cf66; margin: 0 0 10px 0;">📋 Recommended Actions</h4>
            <ul style="color: #f0f4f8; margin: 0; padding-left: 20px; line-height: 1.6;">
                <li>Maintain routine surveillance and reporting</li>
                <li>Monitor trends effectively</li>
            </ul>
        </div>"""

    st.markdown(banner_html, unsafe_allow_html=True)
    st.markdown(action_html, unsafe_allow_html=True)


# Container for the Heatmap visualization
with st.container():
    st.markdown("<h2 style='color: #ffffff; font-weight: 800; margin-bottom: 15px; font-size: 1.8rem;'>Crime Risk Heatmap</h2>", unsafe_allow_html=True)

    # Load dataset if it exists safely using absolute baseline
    data_path = os.path.join(BASE_DIR, "data", "crime_data.csv")
    has_data = os.path.exists(data_path)
    if has_data:
        # pd is already imported at top level, no need to re-import
        df = pd.read_csv(data_path)
        df_filtered = df[(df['hour'] >= hour - 2) & (df['hour'] <= hour + 2)]
        if df_filtered.empty:
            df_filtered = df  # Fallback to full view if no crimes in hour block
            
    # Try rendering the high-performance Folium Heatmap
    try:
        import folium
        from folium.plugins import HeatMap
        from streamlit_folium import st_folium

        # Initialize base map centered at lat, lon inputs with a dark theme to match UI closely
        m = folium.Map(location=[lat, lon], zoom_start=12, tiles='cartodbdark_matter')
        
        # Generate sample points: lat, lon, risk intensity
        heat_data = []
        if has_data:
            np.random.seed(42)  # For consistent simulation
            for _, row in df_filtered.iterrows():
                # Dynamically set risk intensity weight based on prediction logic
                intensity = np.random.uniform(0.7, 1.0) if is_high_risk else np.random.uniform(0.1, 0.4)
                heat_data.append([row['latitude'], row['longitude'], intensity])
        else:
            # Synthesize backup data sample points if no csv exists
            np.random.seed(42)
            spread = 0.035 if is_high_risk else 0.015
            num_pts = 300 if is_high_risk else 80
            for _ in range(num_pts):
                heat_data.append([
                    lat + np.random.randn() * spread, 
                    lon + np.random.randn() * spread, 
                    np.random.uniform(0.6, 1.0) if is_high_risk else np.random.uniform(0.1, 0.4)
                ])

        # Inject Anonymous Reports into Heatmap
        reports_file = os.path.join(BASE_DIR, "data", "reports.csv")
        if os.path.exists(reports_file):
            try:
                reports_df = pd.read_csv(reports_file)
                if 'latitude' in reports_df.columns and 'longitude' in reports_df.columns:
                    valid_reports = reports_df.dropna(subset=['latitude', 'longitude'])
                    for _, r in valid_reports.iterrows():
                        # Intense 1.0 red heat dot
                        heat_data.append([r['latitude'], r['longitude'], 1.0])
                        # Distinct clickable physical marker
                        folium.Marker(
                            location=[r['latitude'], r['longitude']],
                            popup=f"Alert: {r['crime_type']}",
                            icon=folium.Icon(color="red", icon="warning-sign")
                        ).add_to(m)
            except Exception:
                pass

        # Use color gradient: green → yellow → red
        gradient = {0.2: '#00ff00', 0.5: '#ffff00', 1.0: '#ff0000'}
        
        # Overlay heatmap (radius and blur tuned for smoothness and perfect visibility)
        HeatMap(heat_data, gradient=gradient, radius=20, blur=15, max_zoom=1).add_to(m)

        # Display inside Streamlit (returned_objects=[] ensures NO LAG during frontend-backend interaction processing)
        st_folium(m, width=1200, height=450, returned_objects=[])

        if has_data:
            st.markdown("<div style='text-align: right; color: rgba(255,255,255,0.4); font-size: 0.85rem; margin-top: 15px; font-style: italic;'>Folium Heatmap displaying smoothly from data/crime_data.csv</div>", unsafe_allow_html=True)

    except ImportError:
        # Graceful fallback so there are no crashes locally awaiting pip installation
        st.warning("🔄 Upgrading Map Analytics... `folium` and `streamlit-folium` dependencies are missing. Displaying standard map. Run `pip install folium streamlit-folium` to enable the advanced Heatmap.")
        
        spread = 0.035 if is_high_risk else 0.015
        num_points = 1200 if is_high_risk else 300
        df_map = pd.DataFrame({'lat': np.random.randn(num_points) * spread + lat, 'lon': np.random.randn(num_points) * spread + lon}) if not has_data else df_filtered[['latitude', 'longitude']].rename(columns={'latitude': 'lat', 'longitude': 'lon'})
        st.map(df_map, zoom=11, use_container_width=True)

# --- NEW: Location-Based Emergency Contact Feature ---
# Calculate this on every rerun to ensure 'Manual Simulation' works instantly
u_lat = loc['coords']['latitude'] if (loc and 'coords' in loc) else lat
u_lon = loc['coords']['longitude'] if (loc and 'coords' in loc) else lon
responder = get_nearest_responder(u_lat, u_lon)
is_gps_tracked = (loc is not None and 'coords' in loc)

# Show SOS button if Risk is High (either from prediction OR if user is exploring a night-time scenario)
is_dangerous_time = (hour >= 21 or hour <= 5)
should_show_sos = (st.session_state.prediction_made and risk_level == 2) or (is_dangerous_time and (city != "Custom (Chicago / Other)"))

if should_show_sos:
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("<h3 style='color: #ff6b6b; font-weight: 600; margin-bottom: 1rem;'>🚨 Local Emergency Contact</h3>", unsafe_allow_html=True)

    
    if responder is not None:
        st.markdown(f"""
        <a href="tel:{responder['phone']}" style="text-decoration: none;">
            <div style="background: linear-gradient(90deg, #dc3545, #b02a37); 
                        color: white; padding: 25px; border-radius: 12px; 
                        text-align: center; box-shadow: 0 10px 40px rgba(220, 53, 69, 0.4); 
                        cursor: pointer; transition: all 0.3s ease; border: 2px solid rgba(255,255,255,0.2);">
                <h2 style="color: white; margin: 0; font-weight: 900; letter-spacing: 2px;">🆘 SOS: CALL {responder['contact_name'].upper()}</h2>
                <div style="font-size: 0.85rem; color: rgba(255,255,255,0.8); margin-top: 5px; font-weight: 600;">
                    {'📍 LIVE GPS DETECTED' if is_gps_tracked else '🗺️ SYNCED TO MAP'} | NEAREST HUB: {responder['area'].upper()}
                </div>
                <div style="font-size: 0.75rem; color: #ffc107; margin-top: 8px; text-decoration: underline; cursor: pointer;">
                    (Tap to force location refresh if incorrect)
                </div>
            </div>
        </a>
        
        <style>
            div:hover {{ transform: scale(1.02); filter: brightness(1.1); }}
        </style>
        """, unsafe_allow_html=True)
    else:
        # Fallback if no CSV or match found
        st.markdown("""
        <div style="background: rgba(255, 255, 255, 0.05); border: 1px dashed rgba(255,255,255,0.2); 
                    border-radius: 10px; padding: 20px; text-align: center;">
            <p style="margin: 0; color: #a0aec0;">No local responders found for your specific area. Please use the general emergency helpline below.</p>
        </div>
        """, unsafe_allow_html=True)

