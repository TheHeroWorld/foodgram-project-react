from django.contrib import admin

from .models import Cart, Favorite, Ingredient, Recipe, RecipeIngredient, Tag


class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')
    search_fields = ('user',)
    list_filter = ('user', 'recipe')
    empty_value_display = '-пусто-'


class IngredientInLine(admin.StackedInline):
    model = RecipeIngredient


class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'text', 'author', 'id', 'favorite_count', 'ingredients'
    )
    search_fields = ('name', 'text', 'author', 'tags')
    list_filter = ('name', 'tags')
    empty_value_display = '-пусто-'
    inlines = (IngredientInLine,)

    def favorite_count(self, obj):
        return obj.favorites.count()

    favorite_count.short_description = 'Добавлений в избранное'

    def ingredients(self, obj):
        return ', '.join(
            (ingredient for value in
             obj.recipe_ingredients.values_list('ingredient__name')
             for ingredient in value)
        )

    ingredients.short_description = 'Ингрединеты'


class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'color', 'slug')
    empty_value_display = '-пусто-'


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit')
    empty_value_display = '-пусто-'


class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')
    search_fields = ('user',)
    list_filter = ('user', 'recipe')
    empty_value_display = '-пусто-'


admin.site.register(Favorite, FavoriteAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Cart, CartAdmin)

admin.site.site_title = 'Админ-панель foodgram`а'
admin.site.site_header = 'Админ-панель foodgram`а'
