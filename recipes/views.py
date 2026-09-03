from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import models
from .models import (Recipe,Category,Review,RecipeLike, SavedRecipe)
from django.core.paginator import Paginator
from .models import Recipe, Category, Review

# ==========================================
# HOME
# ==========================================

def home(request):

    featured_recipes = Recipe.objects.select_related(
        'category',
        'author'
    ).order_by('-created_at')[:6]

    categories = Category.objects.all().order_by('name')

    return render(
        request,
        'home/home.html',
        {
            'featured_recipes': featured_recipes,
            'categories': categories,
        }
    )
# ==========================================
# REGISTER
# ==========================================

def register(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if not username or not email or not password:
            messages.error(
                request,
                'Please fill in all fields.'
            )
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(
                request,
                'Username already exists.'
            )
            return redirect('register')

        User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        messages.success(
            request,
            'Registration successful. Please login.'
        )

        return redirect('login')

    return render(
        request,
        'accounts/register.html'
    )


# ==========================================
# LOGIN
# ==========================================

def login_view(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            messages.success(
                request,
                'Login successful!'
            )

            return redirect('home')

        messages.error(
            request,
            'Invalid username or password.'
        )

    return render(
        request,
        'accounts/login.html'
    )


# ==========================================
# LOGOUT
# ==========================================

@login_required
def logout_view(request):

    logout(request)

    messages.success(
        request,
        'You have been logged out.'
    )

    return redirect('home')


# ==========================================
# RECIPE LIST
# ==========================================

def recipe_list(request):

    recipes = Recipe.objects.select_related(
        'category',
        'author'
    ).order_by('-created_at')

    search_query = request.GET.get(
        'q',
        ''
    ).strip()

    category_id = request.GET.get(
        'category',
        ''
    )

    # Search
    if search_query:

        recipes = recipes.filter(
            title__icontains=search_query
        )


    # Category filter
    if category_id:

        recipes = recipes.filter(
            category_id=category_id
        )


    # Pagination
    paginator = Paginator(
        recipes,
        9
    )

    page_number = request.GET.get(
        'page'
    )

    page_obj = paginator.get_page(
        page_number
    )


    categories = Category.objects.all().order_by(
        'name'
    )


    return render(
        request,
        'recipes/recipe_list.html',
        {
            'recipes': page_obj,
            'page_obj': page_obj,
            'categories': categories,
            'search_query': search_query,
            'selected_category': category_id,
        }
    )
# ==========================================
# RECIPE DETAIL
# ==========================================

def recipe_detail(request, id):

    recipe = get_object_or_404(
        Recipe,
        id=id
    )

    reviews = Review.objects.filter(
        recipe=recipe
    ).select_related(
        'user'
    ).order_by(
        '-created_at'
    )

    user_liked = False
    user_saved = False
    user_review = None

    if request.user.is_authenticated:

        user_liked = RecipeLike.objects.filter(
            recipe=recipe,
            user=request.user
        ).exists()

        user_saved = SavedRecipe.objects.filter(
            recipe=recipe,
            user=request.user
        ).exists()

        user_review = Review.objects.filter(
            recipe=recipe,
            user=request.user
        ).first()

    return render(
        request,
        'recipes/recipe_detail.html',
        {
            'recipe': recipe,
            'reviews': reviews,
            'user_liked': user_liked,
            'user_saved': user_saved,
            'user_review': user_review,
        }
    )
# ==========================================
# MY RECIPES
# ==========================================

@login_required
def my_recipes(request):

    recipes = Recipe.objects.filter(
        author=request.user
    ).select_related(
        'category'
    ).order_by(
        '-created_at'
    )

    return render(
        request,
        'recipes/my_recipes.html',
        {
            'recipes': recipes,
        }
    )

# ==========================================
# ADD RECIPE
# ==========================================

@login_required
def add_recipe(request):

    categories = Category.objects.all().order_by('name')

    if request.method == 'POST':

        title = request.POST.get('title', '').strip()
        description = request.POST.get('description', '').strip()
        ingredients = request.POST.get('ingredients', '').strip()
        instructions = request.POST.get('instructions', '').strip()
        category_id = request.POST.get('category')
        image = request.FILES.get('image')


        # Required field validation

        if not title:
            messages.error(
                request,
                'Recipe title is required.'
            )

            return render(
                request,
                'recipes/add_recipe.html',
                {
                    'categories': categories,
                }
            )


        if not description:
            messages.error(
                request,
                'Recipe description is required.'
            )

            return render(
                request,
                'recipes/add_recipe.html',
                {
                    'categories': categories,
                }
            )


        if not ingredients:
            messages.error(
                request,
                'Ingredients are required.'
            )

            return render(
                request,
                'recipes/add_recipe.html',
                {
                    'categories': categories,
                }
            )


        if not instructions:
            messages.error(
                request,
                'Instructions are required.'
            )

            return render(
                request,
                'recipes/add_recipe.html',
                {
                    'categories': categories,
                }
            )


        if not category_id:
            messages.error(
                request,
                'Please select a category.'
            )

            return render(
                request,
                'recipes/add_recipe.html',
                {
                    'categories': categories,
                }
            )


        # Check category exists

        category = get_object_or_404(
            Category,
            id=category_id
        )


        # Image validation

        if image:

            allowed_types = [
                'image/jpeg',
                'image/png',
                'image/webp'
            ]

            if image.content_type not in allowed_types:

                messages.error(
                    request,
                    'Only JPG, PNG, and WEBP images are allowed.'
                )

                return render(
                    request,
                    'recipes/add_recipe.html',
                    {
                        'categories': categories,
                    }
                )


            # Maximum image size = 5 MB

            max_size = 5 * 1024 * 1024

            if image.size > max_size:

                messages.error(
                    request,
                    'Image size must be less than 5 MB.'
                )

                return render(
                    request,
                    'recipes/add_recipe.html',
                    {
                        'categories': categories,
                    }
                )


        # Create recipe

        recipe = Recipe.objects.create(
            title=title,
            description=description,
            ingredients=ingredients,
            instructions=instructions,
            category=category,
            author=request.user,
            image=image
        )


        messages.success(
            request,
            'Recipe added successfully!'
        )

        return redirect(
            'recipe_detail',
            id=recipe.id
        )


    return render(
        request,
        'recipes/add_recipe.html',
        {
            'categories': categories,
        }
    )
# ==========================================
# EDIT RECIPE
# ==========================================

@login_required
def edit_recipe(request, id):

    recipe = get_object_or_404(
        Recipe,
        id=id,
        author=request.user
    )

    categories = Category.objects.all().order_by('name')

    if request.method == 'POST':

        title = request.POST.get(
            'title',
            ''
        ).strip()

        description = request.POST.get(
            'description',
            ''
        ).strip()

        ingredients = request.POST.get(
            'ingredients',
            ''
        ).strip()

        instructions = request.POST.get(
            'instructions',
            ''
        ).strip()

        category_id = request.POST.get(
            'category'
        )

        image = request.FILES.get(
            'image'
        )


        # -------------------------
        # REQUIRED FIELD VALIDATION
        # -------------------------

        if not title:

            messages.error(
                request,
                'Recipe title is required.'
            )

            return render(
                request,
                'recipes/edit_recipe.html',
                {
                    'recipe': recipe,
                    'categories': categories,
                }
            )


        if not description:

            messages.error(
                request,
                'Recipe description is required.'
            )

            return render(
                request,
                'recipes/edit_recipe.html',
                {
                    'recipe': recipe,
                    'categories': categories,
                }
            )


        if not ingredients:

            messages.error(
                request,
                'Ingredients are required.'
            )

            return render(
                request,
                'recipes/edit_recipe.html',
                {
                    'recipe': recipe,
                    'categories': categories,
                }
            )


        if not instructions:

            messages.error(
                request,
                'Instructions are required.'
            )

            return render(
                request,
                'recipes/edit_recipe.html',
                {
                    'recipe': recipe,
                    'categories': categories,
                }
            )


        if not category_id:

            messages.error(
                request,
                'Please select a category.'
            )

            return render(
                request,
                'recipes/edit_recipe.html',
                {
                    'recipe': recipe,
                    'categories': categories,
                }
            )


        # -------------------------
        # CATEGORY VALIDATION
        # -------------------------

        category = get_object_or_404(
            Category,
            id=category_id
        )


        # -------------------------
        # IMAGE VALIDATION
        # -------------------------

        if image:

            allowed_types = [
                'image/jpeg',
                'image/png',
                'image/webp'
            ]

            if image.content_type not in allowed_types:

                messages.error(
                    request,
                    'Only JPG, PNG, and WEBP images are allowed.'
                )

                return render(
                    request,
                    'recipes/edit_recipe.html',
                    {
                        'recipe': recipe,
                        'categories': categories,
                    }
                )


            max_size = 5 * 1024 * 1024

            if image.size > max_size:

                messages.error(
                    request,
                    'Image size must be less than 5 MB.'
                )

                return render(
                    request,
                    'recipes/edit_recipe.html',
                    {
                        'recipe': recipe,
                        'categories': categories,
                    }
                )


        # -------------------------
        # UPDATE RECIPE
        # -------------------------

        recipe.title = title

        recipe.description = description

        recipe.ingredients = ingredients

        recipe.instructions = instructions

        recipe.category = category


        if image:
            recipe.image = image


        recipe.save()


        messages.success(
            request,
            'Recipe updated successfully!'
        )


        return redirect(
            'recipe_detail',
            id=recipe.id
        )


    return render(
        request,
        'recipes/edit_recipe.html',
        {
            'recipe': recipe,
            'categories': categories,
        }
    )
# ==========================================
# DELETE RECIPE
# ==========================================

@login_required
def delete_recipe(request, id):

    recipe = get_object_or_404(
        Recipe,
        id=id,
        author=request.user
    )

    if request.method == 'POST':

        recipe.delete()

        messages.success(
            request,
            'Recipe deleted successfully!'
        )

        return redirect(
            'my_recipes'
        )

    return render(
        request,
        'recipes/delete_recipe.html',
        {
            'recipe': recipe
        }
    )

# ==========================================
# ADD REVIEW
# ==========================================

@login_required
def add_review(request, id):

    recipe = get_object_or_404(
        Recipe,
        id=id
    )

    if request.method == 'POST':

        rating = request.POST.get('rating')
        comment = request.POST.get('comment', '').strip()

        # Check rating exists
        if not rating:

            messages.error(
                request,
                'Please select a rating.'
            )

            return redirect(
                'recipe_detail',
                id=recipe.id
            )

        # Convert rating to integer
        try:
            rating = int(rating)

        except ValueError:

            messages.error(
                request,
                'Invalid rating.'
            )

            return redirect(
                'recipe_detail',
                id=recipe.id
            )

        # Rating must be 1-5
        if rating < 1 or rating > 5:

            messages.error(
                request,
                'Rating must be between 1 and 5.'
            )

            return redirect(
                'recipe_detail',
                id=recipe.id
            )

        # Comment required
        if not comment:

            messages.error(
                request,
                'Please write a comment.'
            )

            return redirect(
                'recipe_detail',
                id=recipe.id
            )

        # Minimum comment length
        if len(comment) < 3:

            messages.error(
                request,
                'Comment must contain at least 3 characters.'
            )

            return redirect(
                'recipe_detail',
                id=recipe.id
            )

        # Check if user already reviewed
        existing_review = Review.objects.filter(
            recipe=recipe,
            user=request.user
        ).first()

        if existing_review:

            messages.error(
                request,
                'You have already reviewed this recipe.'
            )

            return redirect(
                'recipe_detail',
                id=recipe.id
            )

        # Create review
        Review.objects.create(
            recipe=recipe,
            user=request.user,
            rating=rating,
            comment=comment
        )

        messages.success(
            request,
            'Your review was added successfully!'
        )

    return redirect(
        'recipe_detail',
        id=recipe.id
    )

# ==========================================
# LIKE / UNLIKE RECIPE
# ==========================================

@login_required
def like_recipe(request, id):

    recipe = get_object_or_404(
        Recipe,
        id=id
    )

    like = RecipeLike.objects.filter(
        recipe=recipe,
        user=request.user
    ).first()

    if like:

        like.delete()

        messages.success(
            request,
            'Recipe unliked.'
        )

    else:

        RecipeLike.objects.create(
            recipe=recipe,
            user=request.user
        )

        messages.success(
            request,
            'Recipe liked ❤️'
        )

    return redirect(
        'recipe_detail',
        id=recipe.id
    )

# ==========================================
# SAVE / UNSAVE RECIPE
# ==========================================

@login_required
def save_recipe(request, id):

    recipe = get_object_or_404(
        Recipe,
        id=id
    )

    saved_recipe = SavedRecipe.objects.filter(
        recipe=recipe,
        user=request.user
    ).first()

    if saved_recipe:

        saved_recipe.delete()

        messages.success(
            request,
            f'"{recipe.title}" removed from saved recipes.'
        )

    else:

        SavedRecipe.objects.create(
            recipe=recipe,
            user=request.user
        )

        messages.success(
            request,
            f'"{recipe.title}" saved successfully.'
        )

    return redirect(
        'recipe_detail',
        id=recipe.id
    )
# ==========================================
# SAVED RECIPES
# ==========================================

@login_required
def saved_recipes(request):

    saved_recipes = SavedRecipe.objects.filter(
        user=request.user
    ).select_related(
        'recipe',
        'recipe__category',
        'recipe__author'
    ).order_by(
        '-created_at'
    )

    return render(
        request,
        'recipes/saved_recipes.html',
        {
            'saved_recipes': saved_recipes
        }
    )
@login_required
def edit_profile(request):

    user = request.user

    if request.method == 'POST':

        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()

        if not username:
            messages.error(
                request,
                'Username cannot be empty.'
            )

            return redirect('edit_profile')

        # Check whether another user already has this username
        if User.objects.filter(
            username=username
        ).exclude(
            id=user.id
        ).exists():

            messages.error(
                request,
                'That username is already taken.'
            )

            return redirect('edit_profile')

        user.username = username
        user.email = email

        user.save()

        messages.success(
            request,
            'Profile updated successfully!'
        )

        return redirect('profile')

    return render(
        request,
        'accounts/edit_profile.html'
    )
@login_required
def profile(request):

    user = request.user

    recipe_count = Recipe.objects.filter(
        author=user
    ).count()

    saved_count = user.saved_recipes.count()

    review_count = Review.objects.filter(
        user=user
    ).count()

    return render(
        request,
        'accounts/profile.html',
        {
            'profile_user': user,
            'recipe_count': recipe_count,
            'saved_count': saved_count,
            'review_count': review_count,
        }
    )