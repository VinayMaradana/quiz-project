from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from PIL import Image as PilImage
from django.core.files.base import ContentFile
from io import BytesIO
import os

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    
    def __str__(self):
        return self.name

class Recipe(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )
    
    DIFFICULTY_CHOICES = (
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    )
    
    title = models.CharField(max_length=200)
    ingredients = models.TextField()
    instructions = models.TextField()
    cooking_time = models.PositiveIntegerField(validators=[MinValueValidator(1)], help_text="In minutes")
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    image = models.ImageField(upload_to='recipes/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        # Save the model first to ensure the image is stored
        super().save(*args, **kwargs)
        
        if self.image and hasattr(self.image, 'path'):
            try:
                img = PilImage.open(self.image.path)
                
                # Verify the image is valid
                img.verify()
                # Reopen the image after verify (verify closes the file)
                img = PilImage.open(self.image.path)
                
                # Determine the image format from the file extension
                file_extension = os.path.splitext(self.image.name)[1].lower()
                format_map = {
                    '.jpg': 'JPEG',
                    '.jpeg': 'JPEG',
                    '.png': 'PNG',
                    '.gif': 'GIF',
                    '.bmp': 'BMP',
                }
                image_format = format_map.get(file_extension, 'JPEG')  # Default to JPEG if unknown
                
                # Resize if necessary
                if img.height != 200 or img.width != 300:
                    output_size = (300, 200)
                    img = img.convert('RGB')  # Convert to RGB for JPEG compatibility
                    img = img.resize(output_size, PilImage.LANCZOS)
                    buffer = BytesIO()
                    img.save(buffer, format=image_format)
                    # Save the resized image
                    self.image.save(self.image.name, ContentFile(buffer.getvalue()), save=False)
                    super().save(*args, **kwargs)
            except Exception as e:
                # Log the error (optional) and skip resizing if image is invalid
                print(f"Error processing image for recipe {self.title}: {str(e)}")
    