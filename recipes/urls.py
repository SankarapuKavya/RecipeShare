from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('recipes/', views.recipe_list, name='recipe_list'),
    path('recipes/<int:id>/', views.recipe_detail, name='recipe_detail'),
    path('my-recipes/', views.my_recipes, name='my_recipes'),
    path('add-recipe/', views.add_recipe, name='add_recipe'),
    path('edit-recipe/<int:id>/', views.edit_recipe, name='edit_recipe'),
    path(
    'delete-recipe/<int:id>/',
    views.delete_recipe,
    name='delete_recipe'
    ),
    path(
        'recipes/<int:id>/review/',
        views.add_review,
        name='add_review'
    ),
    path(
    'like/<int:id>/',
    views.like_recipe,
    name='like_recipe'
),

path(
    'save/<int:id>/',
    views.save_recipe,
    name='save_recipe'
),
path(
    'saved-recipes/',
    views.saved_recipes,
    name='saved_recipes'
),
path(
    'profile/',
    views.profile,
    name='profile'
),
path(
    'profile/edit/',
    views.edit_profile,
    name='edit_profile'
),
]