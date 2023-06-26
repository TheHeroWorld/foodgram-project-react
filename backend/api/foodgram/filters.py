from django_filters import rest_framework as filters
from rest_framework.filters import SearchFilter

from apps.foodgram.models import Recipe, Tag


class RecipeFilterSet(filters.FilterSet):
    is_favorited = filters.BooleanFilter(method='filter_is_favorited')
    is_in_shopping_cart = filters.BooleanFilter(
        method='filter_is_in_shopping_cart'
    )
    tags = filters.ModelMultipleChoiceFilter(
        method='filter_tags', queryset=Tag.objects.all(), to_field_name='slug'
    )

    class Meta:
        model = Recipe
        fields = (
            'name', 'tags', 'author', 'is_favorited', 'is_in_shopping_cart'
        )

    def filter_is_favorited(self, queryset, field_name, value):
        if value:
            return queryset.filter(favorites__user=self.request.user)
        return queryset

    def filter_is_in_shopping_cart(self, queryset, field_name, value):
        if value:
            return queryset.filter(carts__user=self.request.user)
        return queryset

    @staticmethod
    def filter_tags(queryset, field_name, value):
        if value:
            return queryset.filter(tags__in=value).distinct()
        return queryset


class IngredientFilter(SearchFilter):
    search_param = 'name'
