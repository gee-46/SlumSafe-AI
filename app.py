import streamlit as st
import pandas as pd
import pickle
import folium
from streamlit_folium import st_folium
import os
import datetime

# --- Page configuration ---
st.set_page_config(page_title="SlumSafe AI", page_icon="🚨", layout="wide")

# Directory check for reports
os.makedirs('data', exist_ok=True)
if not os.path.exists('data/reports.csv'):
    df_reports = pd.DataFrame(columns=['Date', 'Location', 'Incident_Type', 'Description'])
    df_reports.to_csv('data/reports.csv', index=False)

# --- Load data and models ---
@st.cache_data
def load_data():
    try:
        return pd.read_csv('data/crime_data.csv')
    except Exception as e:
        return pd.DataFrame()

@st.cache_resource
def load_model():
    try:
        with open('model/model.pkl', 'rb') as f:
            return pickle.load(f)
    except Exception as e:
        return None

df_crime = load_data()
model = load_model()

# --- Sidebar Navigation ---
st.sidebar.title("🚨 SlumSafe AI")
st.sidebar.markdown("**Team PulseX** | InnovateX 4.0")
st.sidebar.markdown("---")
page = st.sidebar.radio("Navigation", ["🏠 Dashboard & Heatmap", "🧠 Predict Crime Risk", "📢 Anonymous Report", "⚠️ Emergency"])

# --- Main Views ---
if page == "🏠 Dashboard & Heatmap":
    st.title("🗺️ Crime Hotspot Heatmap")
    st.markdown("Visualizing the invisible. This interactive heatmap displays recorded incidents with color codes representing time-based risk (🔴 Night / 🟢 Day).")
    
    if not df_crime.empty:
        # Default map center
        center_lat = df_crime['latitude'].mean()
        center_lon = df_crime['longitude'].mean()
        
        m = folium.Map(location=[center_lat, center_lon], zoom_start=11)
        
        # Taking a manageable sample to render quickly
        sample_df = df_crime.sample(n=min(800, len(df_crime)), random_state=42)
        
        for _, row in sample_df.iterrows():
            hour = row['hour']
            
            # Map hours to risk levels exactly as the model
            if hour >= 22 or hour <= 4:
                risk_color = 'red'
                risk_label = 'High'
            elif 18 <= hour <= 21:
                risk_color = 'orange'
                risk_label = 'Medium'
            else:
                risk_color = 'green'
                risk_label = 'Low'
            
            folium.CircleMarker(
                location=[row['latitude'], row['longitude']],
                radius=4,
                color=risk_color,
                fill=True,
                fill_color=risk_color,
                fill_opacity=0.6,
                popup=f"Hour: {hour}:00 | Risk: {risk_label}"
            ).add_to(m)
            
        st_folium(m, width=1000, height=600)
    else:
        st.warning("No crime mapping data available in data/crime_data.csv.")

elif page == "🧠 Predict Crime Risk":
    st.title("🧠 Crime Risk Prediction")
    st.markdown("Use our Random Forest ML model to evaluate the risk of incidents based on location coordinates and time.")
    
    col1, col2 = st.columns(2)
    with col1:
        # Defaults to chicago area center
        lat = st.number_input("Latitude", value=41.8501, format="%.5f")
        lon = st.number_input("Longitude", value=-87.6682, format="%.5f")
    with col2:
        hour = st.slider("Hour of Day (0-23)", min_value=0, max_value=23, value=12)
        
    if st.button("Predict Risk 🚀", type="primary"):
        if model is not None:
            # model mapping: 2 is High, 1 is Medium, 0 is Low
            pred = model.predict([[lat, lon, hour]])[0]
            if pred == 2:
                st.error("🔴 **HIGH RISK** - High probability of incident occurrence. Exercise caution.")
            elif pred == 1:
                st.warning("🟡 **MEDIUM RISK** - Moderate incident probability. Stay alert.")
            else:
                st.success("🟢 **LOW RISK** - Area is designated as relatively safe for this hour.")
        else:
            st.error("Model not found in 'model/model.pkl'. Please ensure the model is trained.")

elif page == "📢 Anonymous Report":
    st.title("📢 Anonymous Incident Reporting")
    st.markdown("Help us illuminate data-dark zones. Your report is completely anonymous and directly empowers your community.")
    
    with st.form("report_form", clear_on_submit=True):
        location = st.text_input("Approximate Location or Cross-street*", placeholder="E.g. 54th & Halsted")
        incident = st.selectbox("Incident Type", ["Theft", "Assault", "Vandalism", "Suspicious Activity", "Harassment", "Other"])
        desc = st.text_area("Description of Event", placeholder="Please provide any contextual details.")
        
        submitted = st.form_submit_button("Submit Report Anonymously")
        
        if submitted:
            if location.strip() != "":
                new_data = pd.DataFrame({
                    'Date': [datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
                    'Location': [location],
                    'Incident_Type': [incident],
                    'Description': [desc]
                })
                new_data.to_csv('data/reports.csv', mode='a', header=False, index=False)
                st.success("Report submitted successfully! Thank you for making a difference.")
            else:
                st.error("Location field is required to submit a report.")

elif page == "⚠️ Emergency":
    st.title("🚨 Emergency Action")
    st.markdown("If you are in immediate danger or witnessing a life-threatening event, do not use anonymous reporting. Dispatch authorities immediately.")
    
    st.markdown("""
        <div style='text-align: center; margin-top: 60px;'>
            <a href="tel:911" style="
                background-color: #ff4b4b; 
                color: white; 
                padding: 20px 40px; 
                text-align: center; 
                text-decoration: none; 
                display: inline-block; 
                font-size: 32px; 
                font-weight: 800;
                border-radius: 12px;
                box-shadow: 0 4px 6px rgba(0,0,0,0.3);
                transition: transform 0.2s;
            ">🚨 DIAL 911 NOW 🚨</a>
        </div>
    """, unsafe_allow_html=True)
