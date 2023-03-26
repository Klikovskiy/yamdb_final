from django.core.mail import EmailMessage
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import RefreshToken

from api.v1.filters import TitleFilter
from api.v1.mixins import ModelMixinSet
from api.v1.permissions import (IsAdminOrAuthorOrModerator, IsAdminOrStaff,
                                IsAdminOrUserOrReadOnly)
from api.v1.serializers import (CategorySerializer, CommentSerializer,
                                GenreSerializer, GetTokenSerializer,
                                NotAdminSerializer, ReviewSerializer,
                                SignUpSerializer, TitleReadSerializer,
                                TitleWriteSerializer, UsersSerializer)
from api_yamdb.settings import DEFAULT_FROM_EMAIL
from reviews.models import Category, CustomUser, Genre, Review, Title


class APIGetToken(APIView):
    """
    JWT-токен при отправке username и confirmation code.
    """

    def post(self, request):
        serializer = GetTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        user = get_object_or_404(CustomUser, username=data['username'])
        if data.get('confirmation_code') == user.confirmation_code:
            token = RefreshToken.for_user(user).access_token
            return Response(
                {'token': str(token)},
                status=status.HTTP_201_CREATED
            )
        return Response(
            {'confirmation_code': 'Неверный код!'},
            status=status.HTTP_400_BAD_REQUEST
        )


class APISignup(APIView):
    """
    Код подтверждения на email.
    """

    @staticmethod
    def send_email(data):
        email = EmailMessage(
            subject=data['email_subject'],
            body=data['email_body'],
            from_email=DEFAULT_FROM_EMAIL,
            to=[data['to_email']]
        )
        email.send()

    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        email_body = (
            f'Здравствуйте, {user.username}.'
            f'Код доступа к API: {user.confirmation_code}'
        )
        data = {
            'email_body': email_body,
            'to_email': user.email,
            'email_subject': 'Код доступа к API!'
        }
        self.send_email(data)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CategoryViewSet(ModelMixinSet):
    """
    Список всех категорий.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAdminOrAuthorOrModerator,)

    def get_queryset(self):
        review = get_object_or_404(
            Review,
            id=self.kwargs.get('review_id'))
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(
            Review,
            id=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review)


class GenreViewSet(ModelMixinSet):
    """
    Список жанров.
    """
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsAdminOrAuthorOrModerator,)

    def get_queryset(self):
        title = get_object_or_404(
            Title,
            id=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(
            Title,
            id=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class TitleViewSet(ModelViewSet):
    """
    Список всех произведений.
    """
    queryset = Title.objects.annotate(
        rating=Avg('reviews__score')
    ).all()
    permission_classes = (IsAdminOrUserOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitleReadSerializer
        return TitleWriteSerializer


class UsersViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UsersSerializer
    permission_classes = (IsAuthenticated, IsAdminOrStaff,)
    lookup_field = 'username'
    filter_backends = (SearchFilter,)
    search_fields = ('username',)

    @action(
        methods=['GET', 'PATCH'],
        detail=False,
        permission_classes=(IsAuthenticated,),
        url_path='me')
    def get_current_user_info(self, request):
        serializer = UsersSerializer(request.user)
        if request.method == 'PATCH':
            serializer = NotAdminSerializer(
                request.user, data=request.data, partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.data, status=status.HTTP_200_OK)
