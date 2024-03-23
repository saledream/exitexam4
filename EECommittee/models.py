from django.db import models
from django.conf import settings 
from PIL import Image 
from io import BytesIO 
from django.core.files.uploadedfile import InMemoryUploadedFile 
import sys 
# from instructor.models import PageCompletion 
from django.dispatch import receiver 
from django.db.models.signals import post_save 

User = settings.AUTH_USER_MODEL 

class Department(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name 
    
class Course(models.Model):
    name = models.CharField(max_length=255) 
    dept = models.ForeignKey(Department, on_delete=models.CASCADE, related_name="courses") 
    description = models.TextField() 
    image = models.ImageField(upload_to="course_images") 
    instructor = models.ForeignKey(User, on_delete=models.CASCADE, related_name="courses") 
    
    def __str__(self):
        return self.name 
    
    def save(self, *args, **kwargs):
       
       super().save(*args,**kwargs) 
       img = Image.open(self.image.path) 
       if img.height > 300 or img.width > 300:
           output_size = (288,200)
           img.thumbnail(output_size) 
           img.save(self.image.path)  

    

