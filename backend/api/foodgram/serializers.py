from django.shortcuts import get_object_or_404
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers, validators

from api.users.serializers import CustomUserSerializer
from apps.foodgram.models import (Cart, Favorite, Ingredient, Recipe,
                                  RecipeIngredient, Tag)


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class RecipeIngredientSerializer(serializers.ModelSerializer):
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit')

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'name', 'measurement_unit',
                  'amount', 'recipe', 'ingredient')
        extra_kwargs = {
            'recipe': {'write_only': True},
            'ingredient': {'write_only': True}
        }
        validators = [validators.UniqueTogetherValidator(
            queryset=RecipeIngredient.objects.all(),
            fields=('recipe', 'ingredient'),
            message='Ингредиенты должны быть уникальными!'
        )]

    def create(self, validated_data):
        return RecipeIngredient.objects.create(**validated_data)


class RecipeSerializer(serializers.ModelSerializer):
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    author = CustomUserSerializer(read_only=True)
    ingredients = RecipeIngredientSerializer(
        source='recipe_ingredients',
        read_only=True,
        many=True
    )
    image = Base64ImageField()
    cooking_time = serializers.IntegerField(min_value=1)

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time'
        )

    def get_is_favorited(self, obj):
        request = self.context.get('request')
        if not request or request.user.is_anonymous:
            return False
        return Favorite.objects.filter(user=request.user, recipe=obj).exists()

    def get_is_in_shopping_cart(self, obj):
        request = self.context.get('request')
        if not request or request.user.is_anonymous:
            return False
        return Cart.objects.filter(user=request.user, recipe=obj).exists()

    @staticmethod
    def save_recipe_ingredients(recipe, ingredients):
        for ingredient in ingredients:
            recipe_ingredient = RecipeIngredientSerializer(
                data={
                    'recipe': recipe.pk,
                    'ingredient': ingredient.get('id'),
                    'amount': ingredient.get('amount')
                }
            )
            recipe_ingredient.is_valid(raise_exception=True)
            recipe_ingredient.save()

    def validate(self, attrs):
        ingredients = self.initial_data.get('ingredients')

        if not ingredients:
            raise serializers.ValidationError(
                {'ingredients': 'Отсутствуют ингридиенты!'}
            )
        for ingredient_item in ingredients:
            get_object_or_404(
                Ingredient, id=ingredient_item.get('id')
            )
            if int(ingredient_item.get('amount')) <= 0:
                raise serializers.ValidationError(
                    {'ingredients': 'Количество ингридиента '
                                    'должно быть больше 0!'}
                )
        attrs['ingredients'] = ingredients
        return attrs

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags_data = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tags_data)
        self.save_recipe_ingredients(recipe, ingredients)
        return recipe

    def update(self, instance, validated_data):
        instance.tags.clear()
        instance.tags.set(validated_data.pop('tags'))
        instance.recipe_ingredients.all().delete()
        self.save_recipe_ingredients(
            instance, validated_data.pop('ingredients')
        )
        return super().update(instance, validated_data)


class ShortRecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class FavoriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Favorite
        fields = ('user', 'recipe')

    def validate(self, attrs):
        if Favorite.objects.filter(
                user=attrs.get('user'), recipe=attrs.get('recipe')
        ).exists():
            raise serializers.ValidationError(
                {'favorite': 'Рецепт уже в избранном!'}
            )
        return attrs

    def to_representation(self, instance):
        return ShortRecipeSerializer(instance=instance.recipe).data


class CartSerializer(serializers.ModelSerializer):

    class Meta:
        model = Cart
        fields = ('user', 'recipe')

    def validate(self, attrs):
        if Cart.objects.filter(
                user=attrs.get('user'), recipe=attrs.get('recipe')
        ).exists():
            raise serializers.ValidationError(
                {'favorite': 'Рецепт уже в корзине!'}
            )
        return attrs

    def to_representation(self, instance):
        return ShortRecipeSerializer(instance=instance.recipe).data
