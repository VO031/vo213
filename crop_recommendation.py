import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import joblib

# Dữ liệu chuẩn (giả định) - ví dụ về điều kiện lý tưởng cho các loại cây trồng
data = {
    'temperature': [27, 25, 30, 22, 28, 26, 29, 24, 27, 23],
    'humidity': [80, 75, 85, 70, 90, 65, 80, 70, 75, 80],
    'soil_moisture': [50, 45, 55, 40, 60, 50, 48, 42, 50, 45],
    'nh3': [1.5, 2.0, 1.8, 2.5, 1.2, 2.2, 1.7, 2.3, 1.9, 2.1],
    'precipitation': [10, 5, 15, 0, 20, 8, 12, 3, 7, 10],
    'crop': ['Lúa nước', 'Khoai môn', 'Súng', 'Lúa nước', 'Súng', 'Khoai môn', 'Lúa nước', 'Khoai môn', 'Súng', 'Lúa nước']
}

# Chuyển thành DataFrame
df = pd.DataFrame(data)

# Mã hóa nhãn (crop) thành số
le = LabelEncoder()
df['crop'] = le.fit_transform(df['crop'])

# Chia dữ liệu thành features (X) và target (y)
X = df[['temperature', 'humidity', 'soil_moisture', 'nh3', 'precipitation']]
y = df['crop']

# Chia dữ liệu thành tập huấn luyện và kiểm tra
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Huấn luyện mô hình Random Forest
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Lưu mô hình và LabelEncoder
joblib.dump(model, 'crop_model.pkl')
joblib.dump(le, 'label_encoder.pkl')

# Hàm dự đoán
def predict_crop(temperature, humidity, soil_moisture, nh3, precipitation):
    # Kiểm tra và điều chỉnh dữ liệu đầu vào
    temperature = min(temperature, 50)  # Giả định nhiệt độ bất thường > 50°C
    nh3 = min(nh3, 5)  # Giả định NH3 bất thường > 5 ppm
    
    # Dự đoán
    input_data = [[temperature, humidity, soil_moisture, nh3, precipitation]]
    prediction = model.predict(input_data)
    crop_name = le.inverse_transform(prediction)[0]
    
    warnings = ''
    if temperature > 50:
        warnings += f'Cảnh báo: Nhiệt độ {temperature}°C quá cao, đã điều chỉnh về {min(temperature, 50)}°C.\n'
    if nh3 > 5:
        warnings += f'Cảnh báo: Nồng độ NH3 ({nh3} ppm) quá cao, đã điều chỉnh về {min(nh3, 5)} ppm.\n'
    
    return {'crop': crop_name, 'warnings': warnings}