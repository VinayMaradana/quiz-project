# recipes/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from recipe.models import Recipe, Category
from .forms import RecipeForm, SignUpForm
from django.db.models import Q

class RecipeListView(View):
    def get(self, request):
        categories = Category.objects.all()
        category_id = request.GET.get('category')
        search_query = request.GET.get('q')
        
        recipes = Recipe.objects.filter(status='approved')
        if request.user.is_authenticated:
            recipes = recipes | Recipe.objects.filter(author=request.user)
        
        if category_id:
            recipes = recipes.filter(category_id=category_id)
        if search_query:
            recipes = recipes.filter(Q(title__icontains=search_query) | Q(category__name__icontains=search_query))
            
        return render(request, 'recipes/recipe_list.html', {
            'recipes': recipes.order_by('-created_at'),
            'categories': categories,
            'search_query': search_query,
        })

class RecipeDetailView(View):
    def get(self, request, pk):
        recipe = get_object_or_404(Recipe, pk=pk)
        if recipe.status != 'approved' and recipe.author != request.user and not request.user.is_staff:
            return redirect('recipe_list')
        return render(request, 'recipes/recipe_detail.html', {'recipe': recipe})

class RecipeCreateView(LoginRequiredMixin, View):
    def get(self, request):
        form = RecipeForm()
        return render(request, 'recipes/recipe_form.html', {'form': form})
    
    def post(self, request):
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.save()
            messages.success(request, 'Recipe submitted for approval!')
            return redirect('recipe_list')
        return render(request, 'recipes/recipe_form.html', {'form': form})

class SignUpView(View):
    def get(self, request):
        form = SignUpForm()
        return render(request, 'registration/signup.html', {'form': form})
    
    def post(self, request):
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Account created successfully! Please log in.')
            return redirect('login')
        return render(request, 'registration/signup.html', {'form': form})