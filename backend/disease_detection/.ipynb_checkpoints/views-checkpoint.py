from django.shortcuts import render
import numpy as np
import tensorflow as tf
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import os
from PIL import Image
import io

# ✅ ML Model Load Karo
MODEL_PATH = os.path.join(os.path.dirname(__file__), "crop_disease_model.h5")
model = tf.keras.models.load_model(MODEL_PATH)

# ✅ Categories (Classes)
CATEGORIES = ["Sugarcane - Red Rot", "Sugarcane - Healthy", "Wheat - Brown Rust", "Rice - Leaf Blast", "Potato - Late Blight"]

@csrf_exempt
def predict_disease(request):
    if request.method == 'POST':
        try:
            # ✅ Image Read Karo
            image_file = request.FILES['image']
            image = Image.open(image_file).convert("RGB")
            image = image.resize((224, 224))
            image = np.array(image) / 255.0  # Normalize
            image = np.expand_dims(image, axis=0)  # Batch Dimension

            # ✅ Prediction
            prediction = model.predict(image)
            predicted_class = np.argmax(prediction, axis=1)[0]
            confidence = float(np.max(prediction))

            return JsonResponse({"predicted_class": CATEGORIES[predicted_class], "confidence": confidence})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "Invalid request method"}, status=405)
