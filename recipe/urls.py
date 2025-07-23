from django.urls import path
from recipe.views.views import *
from recipe.views.forms import *

urlpatterns = [
    path('', RecipeListView.as_view(), name='recipe_list'),
    path('recipe/<int:pk>/', RecipeDetailView.as_view(), name='recipe_detail'),
    path('recipe/new/', RecipeCreateView.as_view(), name='recipe_create'),
    path('signup/',SignUpView.as_view(),name='signup'),
]
