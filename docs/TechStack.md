# 🛠️ SlumSafe AI: Detailed Technical Stack

The architecture of SlumSafe AI is designed for high performance, low-latency community interaction, and data security. Below is the comprehensive breakdown of the technologies used.

---

## 1. Frontend: High-Performance Data Dashboard
We chose a **Python-centric UI** approach to ensure rapid deployment and data-to-visual synchronization.

*   **Streamlit (v1.x):** Used as the core application framework. It enables the creation of a responsive, real-time dashboard that integrates Python backend logic directly with interactive web components.
*   **Custom Vanilla CSS & Glassmorphism:** To elevate the user experience, we injected a custom CSS layer into the Streamlit container. This includes:
    *   **Blur filters & backdrop-filters:** For a modern "Glassmorphism" look in the sidebar.
    *   **Linear Gradients:** Deep midnight-blue aesthetics to match high-tech intelligence themes.
    *   **Animated Transitions:** Subtle hover states for the 1-Tap reporting buttons.

---

## 2. Artificial Intelligence & Machine Learning
The predictive core of the project relies on industry-standard ML libraries.

*   **Scikit-Learn:** Used to design, train, and deploy the **Random Forest Classifier**. This ensemble learning method was chosen for its robustness against over-fitting and its high accuracy in spatial classification.
*   **Pickle:** Utilized for model serialization, allowing the pre-trained `model.pkl` to be loaded in milliseconds during application runtime.
*   **Numpy & Pandas:** The backbone for pre-processing input features (Hour, Latitude, Longitude) before they are fed into the prediction engine.

---

## 3. Geospatial Intelligence & Mapping
Turning raw coordinates into human-readable visual intelligence.

*   **Folium:** A powerful Python library built on **Leaflet.js**. It was used to generate the interactive maps.
*   **HeatMap Plugin:** We integrated the `folium.plugins.HeatMap` module to convert thousands of data points into a smooth, color-graded (Green -> Yellow -> Red) risk intensity overlay.
*   **Streamlit-Folium:** Acts as the bridge component that allows the dynamic Leaflet maps to be rendered and updated within the Streamlit UI.

---

## 4. Native Browser Integration (The JS Bridge)
To achieve the "1-Tap" GPS functionality without browser sandbox issues.

*   **Streamlit-JS-Eval:** A specialized integration layer that allows the Python backend to execute **Vanilla JavaScript** directly in the user's main browser context. 
*   **HTML5 Geolocation API:** Used within the JS-Eval bridge to natively request and retrieve high-precision (GPS-level) coordinates directly from the mobile/desktop hardware.
*   **Query Parameters (st.query_params):** Used in the internal fallback logic to handle state-passing between the client-side JavaScript and the server-side Python logic.

---

## 5. Data Management & Storage
A lightweight, edge-compatible data strategy.

*   **Local CSV Storage:** To maintain decentralization and ensure high-speed read/writes without the overhead of a database server, we utilized CSV-resident data storage for both historical datasets (`crime_data.csv`) and community-generated reports (`reports.csv`).
*   **Automated Data Pipeline:** Custom Python scripts (`fetch_chicago.py` & `gen_india_data.py`) use **Requests** and **Socrata API** to pull real-time crime data from international sources and merge it with local simulations.

---

## 6. DevOps & Version Control
*   **Git & GitHub:** For version control, modular development, and collaborative syncing of the "PulseX" team's contributions.
*   **Environment Management:** A refined `requirements.txt` ensuring that all dependencies (from `scikit-learn` to `streamlit-js-eval`) are consistently deployed in any local or cloud environment.

---

## ⭐ Support

If you found this project interesting:

⭐ Star the repo
🍴 Fork it
💡 Build on it

---

> “The tech stack is built on the philosophy of **Minimal Friction for the End User** and **High Precision for the NGOs.**”
