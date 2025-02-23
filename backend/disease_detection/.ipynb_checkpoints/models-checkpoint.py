from django.db import models

class PredictionHistory(models.Model):
    id = models.AutoField(primary_key=True)
    image = models.ImageField(upload_to="predictions/")
    predicted_disease = models.CharField(max_length=255)
    confidence = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.predicted_disease} ({self.confidence}%)"


# Disease Ki Extra Details Store Karne Ka Model
class DiseaseDetail(models.Model):
    disease_name = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    causes = models.TextField()
    symptoms = models.TextField()
    prevention = models.TextField()
    treatment = models.TextField()

    def __str__(self):
        return self.disease_name

