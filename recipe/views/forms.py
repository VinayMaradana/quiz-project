# recipes/forms.py
from django import forms
from recipe.models import Recipe, Category
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['title', 'ingredients', 'instructions', 'cooking_time', 'difficulty', 'category', 'image']
        widgets = {
            'ingredients': forms.Textarea(attrs={'rows': 4}),
            'instructions': forms.Textarea(attrs={'rows': 6}),
        }
    
    def clean_cooking_time(self):
        cooking_time = self.cleaned_data['cooking_time']
        if cooking_time <= 0:
            raise forms.ValidationError("Cooking time must be greater than 0")
        return cooking_time

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text="Required. Enter a valid email address.")
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']