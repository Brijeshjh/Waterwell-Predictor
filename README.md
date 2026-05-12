# AI-Enabled Waterwell Predictor 💧

An intelligent web application that predicts hydrogeological formations and water levels to determine construction suitability and recommends optimal drilling methods based on geographic coordinates.

![Dashboard Screenshot](screenshot.png)

## 🌟 Features

* **🌍 Geological Prediction**: Accurately predicts the underlying hydrogeological formation and provides its classification code.
* **💧 Water Level Prediction**: Estimates the post-2021 water level in meters below ground level (mbgl).
* **🏗️ Construction Suitability**: Automatically evaluates the site's suitability for construction (Excellent, Good, Fair, or Poor) based on predicted water levels.
* **🛠️ Drilling Recommendations**: Suggests the safest and most efficient drilling methods (e.g., Rotary drilling, Auger, Down-the-hole hammer) depending on the rock formation.

## 🚀 Live Demo
*(You can place your deployed Streamlit Cloud link here once it's live!)*

## 💻 Tech Stack
* **Frontend/UI:** [Streamlit](https://streamlit.io/)
* **Machine Learning:** Scikit-Learn (KNeighborsClassifier, RandomForestRegressor)
* **Data Manipulation:** Pandas, NumPy
* **Language:** Python 3

## 🛠️ Running Locally

1. **Clone the repository:**
   ```bash
   git clone https://github.com/YourUsername/Waterwell-Predictor.git
   cd Waterwell-Predictor
   ```

2. **Install the dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Streamlit Dashboard:**
   ```bash
   streamlit run streamlit_app.py
   ```

4. **Open your browser:**
   Navigate to `http://localhost:8501` to view the app!

## 📂 Dataset Details
This model was trained using hydrogeological datasets (`newRajstanHydro.csv` and `NewRajstanChannged.csv`), leveraging historical water levels and geographical attributes.
