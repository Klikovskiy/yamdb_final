from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from user.models import CustomUser

from api_yamdb.settings import USER_CHARFIELD_LENGTH, USER_EMAIL_LENGTH
from reviews.models import Category, Comment, Genre, Review, Title


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        exclude = ('id',)
        model = Category
        lookup_field = 'slug'


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Comment


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        exclude = ('id',)
        model = Genre
        lookup_field = 'slug'


class GetTokenSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        required=True)
    confirmation_code = serializers.CharField(
        required=True)

    class Meta:
        model = CustomUser
        fields = (
            'username',
            'confirmation_code'
        )


class NotAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role'
        )
        read_only_fields = ('role',)


class ReviewSerializer(serializers.ModelSerializer):
    title = serializers.SlugRelatedField(
        slug_field='name',
        read_only=True
    )
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    score = serializers.IntegerField(
        validators=[
            MinValueValidator(1, 'Оценка должна быть не меньше 1.'),
            MaxValueValidator(10, 'Оценка должна быть не больше 10.')
        ],
    )

    def validate(self, data):
        author = self.context['request'].user
        title_id = self.context.get('view').kwargs.get('title_id')
        if (
                self.context['request'].method == 'POST'
                and author.reviews.filter(title_id=title_id).exists()
        ):
            raise ValidationError(
                'На одно произведений можно написать только 1 отзыв!'
            )
        return data

    class Meta:
        fields = ('id', 'title', 'text', 'author', 'score', 'pub_date')
        model = Review


class SignUpSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        max_length=USER_CHARFIELD_LENGTH,
        required=True,
        validators=[UniqueValidator(queryset=CustomUser.objects.all())]
    )

    email = serializers.EmailField(
        max_length=USER_EMAIL_LENGTH,
        required=True,
        validators=[UniqueValidator(queryset=CustomUser.objects.all())]
    )

    def validate_username(self, username):
        if username == 'me':
            raise serializers.ValidationError(
                "Использование 'me' в качестве username нельзя."
            )
        return username

    class Meta:
        model = CustomUser
        fields = ('email', 'username')


class TitleReadSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(
        read_only=True,
        many=True
    )
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        fields = (
            'id',
            'name',
            'year',
            'rating',
            'description',
            'genre',
            'category'
        )
        model = Title


class TitleWriteSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug'
    )
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        many=True
    )

    class Meta:
        fields = (
            'id',
            'name',
            'year',
            'description',
            'genre',
            'category'
        )
        model = Title


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role'
        )
