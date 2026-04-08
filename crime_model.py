import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import pickle
import os

def train_model():
    print("Loading data...")
    df = pd.read_csv('data/crime_data.csv')
    
    # Create target column "risk" with 3 distinct classes mapping to README
    def determine_risk(h):
        if h >= 22 or h <= 4:
            return 2  # High Risk (Night)
        elif 18 <= h <= 21:
            return 1  # Medium Risk (Evening)
        else:
            return 0  # Low Risk (Daytime)

    df['risk'] = df['hour'].apply(determine_risk)
    
    # Features
    X = df[['latitude', 'longitude', 'hour']]
    y = df['risk']
    
    print("Training RandomForestClassifier...")
    # Ensuring fast execution as requested previously
    model = RandomForestClassifier(n_estimators=20, max_depth=5, random_state=42)
    model.fit(X, y)
    
    print("Saving model...")
    os.makedirs('model', exist_ok=True)
    with open('model/model.pkl', 'wb') as f:
        pickle.dump(model, f)
        
    print("Model successfully trained and saved to model/model.pkl")

def predict_risk(lat, lon, hour):
    """
    Predicts if the risk is high, medium, or low for a given location and hour.
    """
    with open('model/model.pkl', 'rb') as f:
        model = pickle.load(f)
    
    # Using a nested list as input matches sklearn expectations without pandas overhead
    prediction = model.predict([[lat, lon, hour]])
    if prediction[0] == 2:
        return "high risk"
    elif prediction[0] == 1:
        return "medium risk"
    else:
        return "low risk"

if __name__ == "__main__":
    train_model()
    
    # Test our prediction function quickly
    test_lat, test_lon, test_hour = 41.85, -87.66, 19
    res = predict_risk(test_lat, test_lon, test_hour)
    print(f"Sample Prediction for Lat: {test_lat}, Lon: {test_lon}, Hour: {test_hour} -> {res}")
