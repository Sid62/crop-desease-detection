from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import numpy as np
import tensorflow as tf
from PIL import Image, UnidentifiedImageError
import os
from .models import PredictionHistory, DiseaseDetail
from .solutions import SOLUTION_RECOMMENDATIONS

# BASE_DIR: current directory of this views.py file
BASE_DIR = os.path.dirname(__file__)
MODELS_DIR = os.path.join(BASE_DIR, "models")

CROP_MODEL_PATHS = {
    "Corn": os.path.join(MODELS_DIR, "corn_disease_model.h5"),
    "Potato": os.path.join(MODELS_DIR, "potato_disease_model.h5"),
    "Rice": os.path.join(MODELS_DIR, "rice_disease_model.h5"),
    "Sugarcane": os.path.join(MODELS_DIR, "sugarcane_disease_model.h5"),
    "Wheat": os.path.join(MODELS_DIR, "wheat_disease_model.h5")
}

CROP_CLASS_LABELS = {
    "Corn": ["Corn___Common_Rust", "Corn___Gray_Leaf_Spot", "Corn___Healthy", "Corn___Northern_Leaf_Blight"],
    "Potato": ["Potato___Early_Blight", "Potato___Late_Blight", "Potato___Healthy"],
    "Rice": ["Rice___Brown_Spot", "Rice___Healthy", "Rice___Leaf_Blast", "Rice___Neck_Blast"],
    "Sugarcane": ["Sugarcane__Bacterial Blight", "Sugarcane___Healthy", "Sugarcane__Red_Rot"],
    "Wheat": ["Wheat___Brown_Rust", "Wheat___Healthy", "Wheat___Yellow_Rust"]
}

solutions = {
    "Corn___Common_Rust": "Use fungicides containing azoxystrobin or propiconazole. Rotate crops to prevent recurrence.",
    "Corn___Gray_Leaf_Spot": "Apply foliar fungicides like pyraclostrobin and practice crop rotation.",
    "Corn___Healthy": "No action needed. Maintain proper irrigation and soil health.",
    "Corn___Northern_Leaf_Blight": "Use resistant corn varieties and fungicides like tebuconazole.",
    
    "Potato___Early_Blight": "Use copper-based fungicides and practice crop rotation.",
    "Potato___Healthy": "No action required. Maintain optimal growing conditions.",
    "Potato___Late_Blight": "Apply fungicides containing mancozeb or chlorothalonil. Ensure good air circulation.",
    
    "Rice___Brown_Spot": "Use potassium fertilizer and apply fungicides like carbendazim.",
    "Rice___Healthy": "No treatment needed. Maintain field hygiene.",
    "Rice___Leaf_Blast": "Apply tricyclazole-based fungicides and use disease-free seeds.",
    "Rice___Neck_Blast": "Use balanced nitrogen fertilizers and apply systemic fungicides.",
    
    "Wheat___Brown_Rust": "Spray fungicides like propiconazole or mancozeb at the first sign of disease.",
    "Wheat___Healthy": "No treatment required. Ensure proper irrigation and soil fertility.",
    "Wheat___Yellow_Rust": "Apply fungicides such as tebuconazole and practice resistant variety plantation.",
    
    "Sugarcane__Red_Rot": "Destroy affected plants, improve drainage, and use disease-resistant varieties.",
    "Sugarcane__Healthy": "No action required. Maintain good field management.",
    "Sugarcane__Bacterial Blight": "Use copper-based bactericides and improve air circulation.",
}

@csrf_exempt
def predict_disease(request):
    if request.method != 'POST':
        return JsonResponse({"error": "Invalid request method. Use POST."}, status=405)
    
    try:
        crop_input = request.POST.get("crop") or request.GET.get("crop")
        if not crop_input:
            return JsonResponse({"error": "Missing crop type."}, status=400)
        
        crop_input = crop_input.strip().lower()
        valid_options = {key.lower(): key for key in CROP_MODEL_PATHS.keys()}
        
        if crop_input not in valid_options:
            return JsonResponse({"error": "Invalid crop type."}, status=400)
        
        crop = valid_options[crop_input]
        model_path = CROP_MODEL_PATHS[crop]

        if not os.path.exists(model_path):
            return JsonResponse({"error": f"Model file not found for crop {crop}."}, status=500)

        model = tf.keras.models.load_model(model_path)

        image_file = request.FILES.get("image")
        if not image_file:
            return JsonResponse({"error": "No image provided."}, status=400)

        try:
            image = Image.open(image_file).convert("RGB")
        except UnidentifiedImageError:
            return JsonResponse({"error": "Invalid image format."}, status=400)
        
        image = image.resize((224, 224))
        image = np.array(image) / 255.0  
        image = np.expand_dims(image, axis=0)  

        prediction = model.predict(image)
        predicted_index = int(np.argmax(prediction, axis=1)[0])
        confidence = float(np.max(prediction))

        class_labels = CROP_CLASS_LABELS.get(crop, [])
        if predicted_index >= len(class_labels):
            return JsonResponse({"error": "Invalid prediction output."}, status=500)
        
        predicted_label = class_labels[predicted_index]

        prediction_record = PredictionHistory.objects.create(
            image=image_file,
            predicted_disease=predicted_label,
            confidence=confidence
        )

        return JsonResponse({
            "predicted_class": predicted_label,
            "confidence": confidence,
            "crop": crop,
            "message": "Prediction saved successfully!"
        })

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)


def get_history(request):
    history = PredictionHistory.objects.all().order_by('-timestamp')
    history_data = [
        {
            "id": h.id,
            "image": h.image.url if h.image else None,
            "disease": h.predicted_disease,
            "confidence": h.confidence,
            "timestamp": h.timestamp.strftime("%Y-%m-%d %H:%M:%S")
        }
        for h in history
    ]
    return JsonResponse({"history": history_data})


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
    
##def normalize_disease_name(name):
##    return name.lower().replace(" ", "").replace("_", "")
##
##def get_solution(request, disease_name):
##    print(f"Received request for disease: {disease_name}")
##    normalized_input = normalize_disease_name(disease_name)
##    matched_solution = None
##    matched_key = disease_name  
##    
##    for key, solution in SOLUTION_RECOMMENDATIONS.items():
##        if normalize_disease_name(key) == normalized_input:
##            matched_solution = solution
##            matched_key = key
##            break
##
##    if matched_solution is None:
##        matched_solution = "No solution available for this disease."
##    
##    print(f"Returning solution for {matched_key}: {matched_solution}")
 ##   return JsonResponse({"disease": matched_key, "solution": matched_solution})




def get_solution(request, disease_name):
    solution = solutions.get(disease_name)
    if solution:
        return JsonResponse({"solution": solution})
    return JsonResponse({"error": "Solution not found!"}, status=404)
