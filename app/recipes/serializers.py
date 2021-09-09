from rest_framework import serializers

from core.models import Recipe, Ingredient


class IngredientSerializer(serializers.ModelSerializer):
    """Serialiser for Ingredient models"""

    class Meta:
        model = Ingredient
        fields = ('name',)
        read_only_fields = ('id',)
        ordering = ('name',)


class RecipeSerializer(serializers.ModelSerializer):
    """Serialiser for Recipe models"""

    ingredients = IngredientSerializer(many=True)

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'description', 'ingredients',)
        read_only_fields = ('id',)
        ordering = ('name',)

    def create(self, validated_data):
        """Overridden to allow nested serialisation of ingredients"""
        ingredients_data = validated_data.pop('ingredients', [])
        recipe = Recipe.objects.create(**validated_data)
        for ingredient_data in ingredients_data:
            Ingredient.objects.create(recipe=recipe, **ingredient_data)
        return recipe

    def update(self, instance, validated_data):
        """Overridden to allow nested serialisation of ingredients"""
        updated_ingredients_data = validated_data.pop('ingredients', [])
        super().update(instance, validated_data)
        instance.ingredients.all().delete()
        for ingredient_data in updated_ingredients_data:
            Ingredient.objects.create(recipe=instance, **ingredient_data)
        return instance
