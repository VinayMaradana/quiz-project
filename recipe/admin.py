from django.contrib import admin
from .models import Recipe, Category
from django import forms
from django.core.exceptions import ValidationError
import os

class RecipeAdminForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = '__all__'
    
    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image:
            # Check file extension
            valid_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp']
            ext = os.path.splitext(image.name)[1].lower()
            if ext not in valid_extensions:
                raise ValidationError("Invalid image format. Supported formats: JPG, PNG, GIF, BMP.")
        return image

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']

@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    form = RecipeAdminForm
    list_display = ['title', 'author', 'category', 'status', 'created_at']
    list_filter = ['status', 'category', 'difficulty']
    search_fields = ['title', 'ingredients']
    actions = ['approve_recipes', 'reject_recipes']
    
    def approve_recipes(self, request, queryset):
        queryset.update(status='approved')
    approve_recipes.short_description = "Approve selected recipes"
    
    def reject_recipes(self, request, queryset):
        queryset.update(status='rejected')
    reject_recipes.short_description = "Reject selected recipes"