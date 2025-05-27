from flask import Flask, request, jsonify
import joblib
import os

app = Flask(__name__)

# Define paths to the model and label encoder
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, 'crop_model.pkl')
LABEL_ENCODER_PATH = os.path.join(BASE_DIR, 'label_encoder.pkl')

# Load the model and label encoder
try:
    model = joblib.load(MODEL_PATH)
    le = joblib.load(LABEL_ENCODER_PATH)
except FileNotFoundError as e:
    print(f"Error: {e}. Please ensure 'crop_model.pkl' and 'label_encoder.pkl' are in the same directory as this script.")
    exit(1)

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    temperature = data.get('temperature', 0)
    humidity = data.get('humidity', 0)
    soil_moisture = data.get('soil_moisture', 0)
    nh3 = data.get('nh3', 0)
    precipitation = data.get('precipitation', 0)
    
    # Dự đoán
    temperature = min(temperature, 50)
    nh3 = min(nh3, 5)
    input_data = [[temperature, humidity, soil_moisture, nh3, precipitation]]
    prediction = model.predict(input_data)
    crop_name = le.inverse_transform(prediction)[0]
    
    warnings = ''
    if data.get('temperature', 0) > 50:
        warnings += f'Cảnh báo: Nhiệt độ {data["temperature"]}°C quá cao, đã điều chỉnh về 50°C.\n'
    if data.get('nh3', 0) > 5:
        warnings += f'Cảnh báo: Nồng độ NH3 ({data["nh3"]} ppm) quá cao, đã điều chỉnh về 5 ppm.\n'
    
    return jsonify({'crop': crop_name, 'warnings': warnings})

if __name__ == '__main__':
    app.run(debug=True)