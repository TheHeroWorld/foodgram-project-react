from django.db.models import Sum
from django.http import HttpResponse
from django_filters import rest_framework as filters
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from api.foodgram.serializers import (CartSerializer, IngredientSerializer,
                                      RecipeSerializer, TagSerializer)
from apps.foodgram.models import (Cart, Favorite, Ingredient, Recipe,
                                  RecipeIngredient, Tag)

from .filters import IngredientFilter, RecipeFilterSet
from .pagination import LimitPageNumberPagination
from .permissions import IsOwnerOrReadOnly
from .serializers import FavoriteSerializer


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None
    search_fields = ('^name',)
    filter_backends = (IngredientFilter, )


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    filterset_class = RecipeFilterSet
    permission_classes = (IsOwnerOrReadOnly,)
    filter_backends = (filters.DjangoFilterBackend,)
    pagination_class = LimitPageNumberPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @staticmethod
    def saveobject(request, serializer_class, pk):
        data = {
            'user': request.user.pk,
            'recipe': pk
        }
        serializer = serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @staticmethod
    def deleteobject(request, model, pk):
        recipe = get_object_or_404(Recipe, pk=pk)
        obj = get_object_or_404(model, user=request.user, recipe=recipe)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['post'])
    def favorite(self, request, pk=None):
        return self.saveobject(request, FavoriteSerializer, pk)

    @favorite.mapping.delete
    def delete_favorite(self, request, pk=None):
        return self.deleteobject(request, Favorite, pk)

    @action(detail=True, methods=['post'])
    def shopping_cart(self, request, pk=None):
        return self.saveobject(request, CartSerializer, pk)

    @shopping_cart.mapping.delete
    def delete_shopping_cart(self, request, pk=None):
        return self.deleteobject(request, Cart, pk)

    @staticmethod
    def pdf_shopping_cart(queryset):
        pdfmetrics.registerFont(
            TTFont('ExtraBold', 'extrabold.ttf', 'utf-8'))
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = ('attachment; '
                                           'filename="shopping_cart.pdf"')
        cnv = canvas.Canvas(response)
        cnv.setFont('ExtraBold', 36)
        cnv.drawString(150, 800, "Список покупок.")
        cnv.setFont('ExtraBold', 14)
        text_object = cnv.beginText(100, 750)
        counter = 1
        for ingredient, unit, amount in queryset:
            text_object.textLine(
                f'{counter}. {ingredient} ({unit}) - {amount}'
            )
            counter += 1
        cnv.drawText(text_object)
        cnv.showPage()
        cnv.save()
        return response

    @action(detail=False)
    def download_shopping_cart(self, request):
        queryset = RecipeIngredient.objects.filter(
            recipe__carts__user=request.user
        ).values_list(
            'ingredient__name', 'ingredient__measurement_unit'
        ).annotate(Sum('amount')).order_by('ingredient__name')
        return self.pdf_shopping_cart(queryset)
