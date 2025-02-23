from django.shortcuts import render
import numpy as np
import tensorflow as tf
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import os
from django.shortcuts import get_object_or_404
from .models import PredictionHistory, DiseaseDetail
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

            # ✅ Image Save Karo File System Me
            prediction_record = PredictionHistory.objects.create(
                image=image_file,  # ✅ Image Store Karna
                predicted_disease=CATEGORIES[predicted_class],
                confidence=confidence
            )

            return JsonResponse({
                "predicted_class": CATEGORIES[predicted_class],
                "confidence": confidence,
                "message": "Prediction saved successfully!"
            })
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "Invalid request method"}, status=405)



def get_history(request):
    history = PredictionHistory.objects.all().order_by('-timestamp')
    history_data = [
        {
            "id": h.id,
            "image": h.image.url if h.image else None,  # ✅ Agar image na ho to None return kare
            "disease": h.predicted_disease,
            "confidence": h.confidence,
            "timestamp": h.timestamp.strftime("%Y-%m-%d %H:%M:%S")
        }
        for h in history
    ]
    return JsonResponse({"history": history_data})


# Disease Details Fetch Karne Ka API
def get_disease_details(request, disease_name):
    try:
        disease = DiseaseDetail.objects.get(disease_name=disease_name)
        data = {
            "disease_name": disease.disease_name,
            "description": disease.description,
            "causes": disease.causes,
            "symptoms": disease.symptoms,
            "prevention": disease.prevention,
            "treatment": disease.treatment
        }
        return JsonResponse(data)
    except DiseaseDetail.DoesNotExist:
        return JsonResponse({"error": "Disease details not found!"}, status=404)
