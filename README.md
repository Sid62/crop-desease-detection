# 🌾 Crop Disease Detection

A Machine Learning-based application for detecting crop diseases using images. It helps farmers identify crop diseases and provides additional details about them.

## 🚀 Features
✅ **Disease Prediction** - Upload an image, and the model will predict the disease.
✅ **Past Predictions Storage** - Users can see their previous predictions.
✅ **Extra Disease Details** - Provides additional information about detected diseases.
🚧 **Solution Recommendation** - (Upcoming) Suggests solutions for detected diseases.
🚧 **Feedback System** - (Upcoming) Users can give feedback on predictions.

## 🛠️ Tech Stack
- **Backend:** Django 
- **Machine Learning:** TensorFlow + CNN Model
- **Database:** SQLite
- **Frontend:** (To be integrated)

## 🔧 Installation
1. Clone the repository:
   ```sh
   git clone https://github.com/Sid62/crop-desease-detection.git
   cd crop-desease-detection/backend
   ```
2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
3. Run the backend server:
   ```sh
   uvicorn main:app --reload
   ```
4. API available at: `http://127.0.0.1:8000/`

## 🖼️ Usage
- Use the `/disease_detection/predict/` API to upload an image and get disease predictions.
- Check past predictions at `/past_predictions/`
- Fetch disease details from `/disease_details/{disease_name}/`

## 🤝 Contribution
Feel free to contribute by creating a pull request or reporting issues!
