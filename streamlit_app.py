import streamlit as st
import numpy as np
import pandas as pd
from sklearn import preprocessing
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestRegressor
import warnings
warnings.filterwarnings('ignore')

@st.cache_resource
def load_models():
    # Load data
    hyd_for = pd.read_csv("Dataset/newRajstanHydro.csv")
    df = pd.read_csv("Dataset/NewRajstanChannged.csv")
    
    # Fit LabelEncoder on all available formation types for consistency
    label_encoder = preprocessing.LabelEncoder()
    label_encoder.fit(pd.concat([hyd_for['Hyd_Formation'], df['Hyd_Formation']]))
    
    hyd_for['Hyd_Formation'] = label_encoder.transform(hyd_for['Hyd_Formation'])
    df['Hyd_Formation'] = label_encoder.transform(df['Hyd_Formation'])
    
    # Train Hydrogeological Model (KNeighborsClassifier)
    x_hyd = hyd_for[["Latitude", "Longitude"]]
    y_hyd = hyd_for["Hyd_Formation"]
    model_hyd = KNeighborsClassifier(algorithm='auto', n_neighbors=9, weights='distance')
    model_hyd.fit(x_hyd, y_hyd)
    
    # Train Water Level Model (RandomForestRegressor)
    x_wl = df[["Latitude", "Longitude", "Hyd_Formation"]]
    y_wl = df["Wl_post_2021_m_bbgl"]
    model_wl = RandomForestRegressor(max_features='sqrt', n_estimators=100, random_state=42)
    model_wl.fit(x_wl, y_wl)
    
    return model_hyd, model_wl, label_encoder

st.set_page_config(page_title="Waterwell Predictor", layout="centered")

st.title("AI-Enabled Waterwell Predictor 💧")
st.write("Predict hydrogeological formations and water levels to determine construction suitability and recommended drilling methods.")

# Sidebar for inputs
with st.sidebar:
    st.header("Location Input")
    latitude = st.number_input("Latitude", value=26.6832448, format="%.7f")
    longitude = st.number_input("Longitude", value=75.2335695, format="%.7f")
    predict_button = st.button("Predict 🚀", type="primary")

drill_type = {
    0: "Consist of hard, crystalline rocks --> Rotary drilling with diamond or tungsten carbide bits or Down-the-hole hammer drilling",
    1: "Consist of hard, crystalline rocks --> Rotary drilling with diamond or tungsten carbide bits or Down-the-hole hammer drilling",
    2: "Consist of sand, gravel, and silt --> Auger drilling or Percussion drilling",
    3: "Consist of hard and abrasive rocks --> Rotary drilling with diamond or tungsten carbide bits or Down-the-hole hammer drilling",
    4: "Consist of hard and abrasive rocks --> Rotary drilling with diamond or tungsten carbide bits or Down-the-hole hammer drilling",
    5: "Consist Variation in Hardness --> Rotary drilling with suitable bits or down-the-hole hammer drilling",
    6: "Consist of sand, gravel, and silt --> Auger drilling or Percussion drilling",
    7: "Consist of sand, gravel, and silt --> Auger drilling or Percussion drilling"
}

if predict_button:
    with st.spinner("Loading models and predicting..."):
        try:
            model_hyd, model_wl, label_encoder = load_models()
            
            # Predict Hydrological Formation
            # We supply valid feature names by making it a DataFrame if needed, or just suppress warnings
            hyd_val = np.array([[latitude, longitude]])
            hyd_pred = int(model_hyd.predict(hyd_val)[0])
            
            try:
                formation_name = label_encoder.inverse_transform([hyd_pred])[0]
            except Exception:
                formation_name = f"Unknown Formation Code ({hyd_pred})"
            
            # Predict Water Level
            uservalue = np.array([[latitude, longitude, hyd_pred]])
            wl_pred = model_wl.predict(uservalue)[0]
            
            # Drilling Recommendation
            drilling_method = drill_type.get(hyd_pred, "No specific recommendation available for this formation code.")
            
            # Construction Suitability
            if 0 < wl_pred <= 30:
                suitability = "Excellent for Construction 🟢"
            elif 30 < wl_pred <= 60:
                suitability = "Good for Construction 🟡"
            elif 60 < wl_pred <= 100:
                suitability = "Fair for Construction 🟠"
            else:
                suitability = "Poor for Construction 🔴"
                
            # Display Results
            col1, col2 = st.columns(2)
            
            with col1:
                st.info("### 🌍 Geological Prediction")
                st.write(f"**Formation:** {formation_name}")
                st.write(f"**Formation Code:** {hyd_pred}")
                
            with col2:
                st.success("### 💧 Water Level Prediction")
                st.write(f"**Water Level:** {wl_pred:.2f} m (bbgl)")
                st.write(f"**Suitability:** {suitability}")
                
            st.warning("### 🏗️ Drilling Recommendation")
            st.write(f"**Method:** {drilling_method}")

        except Exception as e:
            st.error(f"An error occurred during prediction: {e}")
else:
    st.info("👈 Enter Latitude and Longitude in the sidebar and click 'Predict' to see the results.")
