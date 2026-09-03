from django.contrib import admin

from .models import Category, Recipe, Review


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):

    list_display = (
        'name',
        'description',
    )

    search_fields = (
        'name',
    )

    ordering = (
        'name',
    )


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):

    list_display = (
        'title',
        'category',
        'author',
        'created_at',
        'updated_at',
    )

    list_filter = (
        'category',
        'created_at',
    )

    search_fields = (
        'title',
        'description',
        'ingredients',
        'instructions',
        'author__username',
    )

    readonly_fields = (
        'created_at',
        'updated_at',
    )

    ordering = (
        '-created_at',
    )


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):

    list_display = (
        'recipe',
        'user',
        'rating',
        'created_at',
    )

    list_filter = (
        'rating',
        'created_at',
    )

    search_fields = (
        'recipe__title',
        'user__username',
        'comment',
    )

    readonly_fields = (
        'created_at',
        'updated_at',
    )

    ordering = (
        '-created_at',
    )