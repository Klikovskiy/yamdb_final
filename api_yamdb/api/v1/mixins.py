from rest_framework.filters import SearchFilter
from rest_framework.mixins import (CreateModelMixin, DestroyModelMixin,
                                   ListModelMixin)
from rest_framework.viewsets import GenericViewSet

from .permissions import IsAdminOrUserOrReadOnly


class ModelMixinSet(
    CreateModelMixin,
    DestroyModelMixin,
    GenericViewSet,
    ListModelMixin,
):
    permission_classes = (IsAdminOrUserOrReadOnly,)
    filter_backends = (SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'
