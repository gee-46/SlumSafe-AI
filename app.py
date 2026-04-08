import streamlit as st
import pandas as pd
import numpy as np

# --- Page Configuration ---
st.set_page_config(
    page_title="SlumSafe AI",
    page_icon="🚨",
    layout="wide",
    initial_sidebar_state="expanded"
)

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
    
    # Input fields
    lat = st.number_input("Latitude", value=41.8781, format="%.4f")
    lon = st.number_input("Longitude", value=-87.6298, format="%.4f")
    
    # Hour slider
    st.markdown("<div style='margin-top: 1rem;'></div>", unsafe_allow_html=True)
    hour = st.slider("Select Hour", min_value=0, max_value=23, value=22, format="%d", help="Select time in 24-hr format")
    
    # Logic to determine risk level
    is_high_risk = (hour >= 20) or (hour <= 4)

    # Predict button
    st.markdown("<div style='margin-top: 1.5rem; margin-bottom: 1.5rem;'></div>", unsafe_allow_html=True)
    predict_clicked = st.button("Predict Risk", key="predict_btn")
    
    # Render Colored Result Box dynamically based on the slider (or button)
    if is_high_risk:
        st.markdown("""
        <div style="background: linear-gradient(135deg, rgba(220, 53, 69, 0.9), rgba(150, 20, 40, 0.8)); 
                    color: white; border-radius: 12px; padding: 18px; text-align: center; 
                    box-shadow: 0 8px 25px rgba(220, 53, 69, 0.4); border: 1px solid rgba(255, 100, 100, 0.2); 
                    margin-bottom: 1rem; transition: transform 0.3s ease;">
            <h4 style='margin:0 0 5px 0; font-weight: 800; text-transform: uppercase; font-size: 1.1rem; letter-spacing: 1px;'>⚠️ High Risk!</h4>
            <p style='margin:0; font-size: 0.95em; opacity: 0.95;'>Zone A is highly active right now</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="background: linear-gradient(135deg, rgba(25, 135, 84, 0.9), rgba(15, 90, 50, 0.8)); 
                    color: white; border-radius: 12px; padding: 18px; text-align: center; 
                    box-shadow: 0 8px 25px rgba(25, 135, 84, 0.4); border: 1px solid rgba(100, 255, 150, 0.2); 
                    margin-bottom: 1rem; transition: transform 0.3s ease;">
            <h4 style='margin:0 0 5px 0; font-weight: 800; text-transform: uppercase; font-size: 1.1rem; letter-spacing: 1px;'>✅ Low Risk</h4>
            <p style='margin:0; font-size: 0.95em; opacity: 0.95;'>Zone A appears safe currently</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<hr>", unsafe_allow_html=True)
    
    # Anonymous Crime Reporting Section
    st.markdown("<h3 style='color: #ffffff; font-weight: 600; margin-bottom: 1.5rem;'>Anonymous Reporting</h3>", unsafe_allow_html=True)
    crime_type = st.selectbox("Crime Type:", ["Theft", "Assault", "Vandalism", "Burglary", "Other"])
    location = st.text_input("Location:", value="Zone A")
    
    st.markdown("<div style='margin-top: 1.5rem;'></div>", unsafe_allow_html=True)
    report_clicked = st.button("Report Anonymously", key="report_btn", help="Submit incident securely and anonymously")
    
    if report_clicked:
        st.markdown(f"""
        <div style="background-color: rgba(255, 255, 255, 0.05); color: #8ec5fc; border-radius: 8px; 
                    padding: 12px; text-align: center; border: 1px solid rgba(142, 197, 252, 0.3); margin-top: 15px;">
            <span style='font-size: 0.9em;'>Recent Report: <b>{crime_type}</b> in <b>{location}</b></span>
        </div>
        """, unsafe_allow_html=True)

# --- Main Panel Content ---

# Alert Banner container logic (Show only if High Risk)
if is_high_risk:
    st.markdown("""
    <div style="background: rgba(220, 53, 69, 0.15); border-left: 6px solid #dc3545; padding: 1.25rem 1.5rem; 
                border-radius: 12px; box-shadow: 0 8px 30px rgba(0,0,0,0.2); margin-bottom: 2.5rem;
                backdrop-filter: blur(10px); border-right: 1px solid rgba(255,255,255,0.05); 
                border-top: 1px solid rgba(255,255,255,0.05); border-bottom: 1px solid rgba(255,255,255,0.05);">
        <div style="display: flex; align-items: center;">
            <span style="font-size: 2rem; margin-right: 20px; filter: drop-shadow(0 2px 5px rgba(220,53,69,0.5));">🚨</span>
            <div>
                <h4 style="color: #ff6b6b; margin: 0 0 5px 0; font-weight: 800; font-size: 1.2rem;">Alert</h4>
                <p style="color: #f0f4f8; margin: 0; font-size: 1.05rem; opacity: 0.9;">High Crime Risk in this area during selected time</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
    <div style="background: rgba(25, 135, 84, 0.15); border-left: 6px solid #198754; padding: 1.25rem 1.5rem; 
                border-radius: 12px; box-shadow: 0 8px 30px rgba(0,0,0,0.2); margin-bottom: 2.5rem;
                backdrop-filter: blur(10px); border-right: 1px solid rgba(255,255,255,0.05); 
                border-top: 1px solid rgba(255,255,255,0.05); border-bottom: 1px solid rgba(255,255,255,0.05);">
        <div style="display: flex; align-items: center;">
            <span style="font-size: 2rem; margin-right: 20px; filter: drop-shadow(0 2px 5px rgba(25,135,84,0.5));">🛡️</span>
            <div>
                <h4 style="color: #51cf66; margin: 0 0 5px 0; font-weight: 800; font-size: 1.2rem;">Safe Zone</h4>
                <p style="color: #f0f4f8; margin: 0; font-size: 1.05rem; opacity: 0.9;">Low Crime Risk in this area during selected time</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


# Container for the Heatmap visualization
with st.container():
    st.markdown("<h2 style='color: #ffffff; font-weight: 800; margin-bottom: 15px; font-size: 1.8rem;'>Crime Risk Heatmap</h2>", unsafe_allow_html=True)

    # Simulated heatmap data logic
    np.random.seed(42)  # For consistent dummy data
    
    # Adjust spread and density based on risk level to showcase visual changes
    spread = 0.035 if is_high_risk else 0.015
    num_points = 1200 if is_high_risk else 300
    
    df_map = pd.DataFrame({
        'lat': np.random.randn(num_points) * spread + lat,
        'lon': np.random.randn(num_points) * spread + lon,
    })

    # Render Streamlit Map
    st.map(df_map, zoom=11, use_container_width=True)
    
    st.markdown("<div style='text-align: right; color: rgba(255,255,255,0.4); font-size: 0.85rem; margin-top: 15px; font-style: italic;'>Data is simulated for demonstration purposes.</div>", unsafe_allow_html=True)
