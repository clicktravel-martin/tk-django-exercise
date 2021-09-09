from rest_framework import viewsets

from recipes.serializers import RecipeSerializer
from core.models import Recipe


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer

    def get_queryset(self):
        """Allow recipes to be filtered by partially-matching name"""
        name_param = self.request.query_params.get('name')
        if name_param:
            return self.queryset.filter(name__icontains=name_param)
        return self.queryset
