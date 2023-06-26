from djoser.views import UserViewSet
from rest_framework import permissions, status
from rest_framework.decorators import action
from rest_framework.generics import ListAPIView, get_object_or_404
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from apps.users.models import Follow, User

from ..foodgram.pagination import LimitPageNumberPagination
from .serializers import CustomUserSerializer, SubscribeSerializer


class CustomUserViewSet(UserViewSet):
    queryset = User.objects.all()
    pagination_class = LimitPageNumberPagination
    serializer_class = CustomUserSerializer

    @action(
        methods=['post'],
        detail=True,
        permission_classes=(permissions.IsAuthenticated,)
    )
    def subscribe(self, request, id=None):
        serializer = SubscribeSerializer(
            data={'user': request.user.id, 'author': id},
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @subscribe.mapping.delete
    def delete_subscribe(self, request, id=None):
        author = get_object_or_404(User, id=id)
        follow = get_object_or_404(Follow, user=request.user, author=author)
        follow.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SubscribeViewSet(ListAPIView, GenericViewSet):
    pagination_class = LimitPageNumberPagination
    queryset = Follow.objects.all()
    serializer_class = SubscribeSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def list(self, request, *args, **kwargs):
        queryset = request.user.follower.all()
        pages = self.paginate_queryset(queryset)
        serializer = SubscribeSerializer(
            instance=pages,
            many=True,
            context={'request': request}
        )
        return self.get_paginated_response(serializer.data)
