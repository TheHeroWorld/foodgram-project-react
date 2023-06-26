from djoser.serializers import (UserCreateSerializer, UserSerializer,
                                serializers)

from apps.foodgram.models import Recipe
from apps.users.models import Follow, User


class CustomUserCreateSerializer(UserCreateSerializer):
    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'password'
        )
        extra_kwargs = {
            'email': {'required': True},
            'username': {'required': True},
            'password': {'required': True, 'write_only': True},
            'first_name': {'required': True},
            'last_name': {'required': True}
        }


class CustomUserSerializer(UserSerializer):
    is_subscribed = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed'
        )

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if not request or request.user.is_anonymous:
            return False
        return obj.following.filter(user=request.user).exists()


class AuthorRecipeSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    name = serializers.ReadOnlyField()
    image = serializers.ImageField()
    cooking_time = serializers.ReadOnlyField()

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class SubscribeSerializer(serializers.ModelSerializer):
    recipes = serializers.SerializerMethodField(read_only=True)
    recipes_count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Follow
        fields = ('user', 'author', 'recipes', 'recipes_count')
        extra_kwargs = {
            'user': {'write_only': True},
            'author': {'write_only': True}
        }

    def validate(self, attrs):
        user = attrs['user']
        author = attrs['author']
        if user == author:
            raise serializers.ValidationError(
                {'follow': 'Нельзя подписываться на себя!'}
            )
        if author.following.filter(user=user).exists():
            raise serializers.ValidationError(
                {'follow': 'Вы уже подписаны на этого пользователя!'}
            )
        return attrs

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        user_data = CustomUserSerializer(
            instance=instance.author,
            context={'request': self.context['request']}
        ).data
        user_data.update(representation)
        return user_data

    def get_recipes(self, obj):
        request = self.context.get('request')
        if not request:
            serializers.ValidationError(
                {'context': 'Отсутствует обязательный ключ request'}
            )
        recipes_limit = request.query_params.get('recipes_limit', None)
        queryset = obj.author.recipes.all()
        if recipes_limit:
            queryset = queryset[:int(recipes_limit)]
        return AuthorRecipeSerializer(queryset, many=True).data

    @staticmethod
    def get_recipes_count(obj):
        return obj.author.recipes.count()
