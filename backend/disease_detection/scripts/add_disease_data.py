import django
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
django.setup()

from disease_detection.models import DiseaseDetail

# ✅ Disease Data Insert Karna
disease_data = [
    {
        "disease_name": "Wheat - Brown Rust",
        "description": "A fungal disease affecting wheat crops.",
        "causes": "Caused by the fungus Puccinia triticina.",
        "symptoms": "Small brown spots on leaves.",
        "prevention": "Use resistant wheat varieties.",
        "treatment": "Apply fungicides."
    },
    {
        "disease_name": "Sugarcane - Red Rot",
        "description": "A severe fungal disease of sugarcane.",
        "causes": "Caused by the fungus Colletotrichum falcatum.",
        "symptoms": "Drying of leaves, red streaks in stalks.",
        "prevention": "Use disease-free seed cane.",
        "treatment": "Use fungicidal sprays."
    }
]

for data in disease_data:
    DiseaseDetail.objects.update_or_create(
        disease_name=data["disease_name"],
        defaults=data
    )

print("✅ Disease details added successfully!")
