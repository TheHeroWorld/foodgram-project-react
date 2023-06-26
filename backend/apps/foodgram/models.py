from django.conf import settings
from django.core.validators import MinValueValidator, UniqueValidator
from django.db import models

from ..users.models import User

LENGHT = 7
REC = "recipes"
INGRED = "recipe_ingredients"
CART = "carts"
FAV = "favorites"


class Ingredient(models.Model):
    name = models.CharField(
        'Наименование',
        max_length=settings.DEFAULT_MAX_LENGTH,
        db_index=True
    )
    measurement_unit = models.CharField(
        'ед. изм',
        max_length=settings.DEFAULT_MAX_LENGTH,
        db_index=True
    )

    class Meta:
        ordering = ('-id',)
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(
        'Наименование',
        max_length=settings.DEFAULT_MAX_LENGTH,
        blank=False,
        unique=True
    )
    color = models.CharField(
        'Цвет',
        max_length=LENGHT,
        blank=False,
        unique=True
    )
    slug = models.SlugField('Slug', blank=False, unique=True)

    class Meta:
        ordering = ('-id',)
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        related_name=REC,
        on_delete=models.CASCADE,
        verbose_name='Автор'
    )
    name = models.CharField(
        'Наименование',
        max_length=settings.DEFAULT_MAX_LENGTH,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    image = models.ImageField(upload_to='recipes/', verbose_name='Картинка')
    text = models.TextField('Описание рецепта')
    tags = models.ManyToManyField(Tag, verbose_name='Теги')
    cooking_time = models.PositiveSmallIntegerField(
        'Время приготовления',
        validators=(MinValueValidator(settings.MIN_VALUE_TO_INT_FIELD),)
    )

    class Meta:
        ordering = ('-id',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name=INGRED,
        verbose_name='Рецепт'
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name='Ингредиент'
    )
    amount = models.PositiveSmallIntegerField(
        'Количество',
        validators=(MinValueValidator(settings.MIN_VALUE_TO_INT_FIELD),)
    )

    class Meta:
        ordering = ('-id',)
        verbose_name = 'Ингредиенты рецепта'
        verbose_name_plural = 'Ингредиенты рецептов'

    def __str__(self):
        return f'{self.recipe.name} - {self.ingredient.name}: {self.amount}'


class Cart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Покупатель',
        related_name=CART
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
    )

    class Meta:
        ordering = ('-id',)
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Покупки'

    def __str__(self):
        return f'{self.user.username} - {self.recipe.name}'


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        related_name=FAV,
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт'
    )

    class Meta:
        ordering = ('-id',)
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'

    def __str__(self):
        return f'{self.user.username} - {self.recipe.name}'

    @property
    def cooking_time(self):
        return self.recipe.cooking_time
