from django.test import TestCase

from core.models import Recipe, Ingredient


class ModelTests(TestCase):

    def test_recipe_string_representation(self):
        """Test a recipe's string representation"""
        recipe = Recipe.objects.create(name='Beans on toast')

        self.assertEqual(str(recipe), 'Beans on toast')

    def test_ingredient_string_representation(self):
        """Test an ingredient's string representation"""
        recipe = Recipe.objects.create(name='Chicken chow mein')
        ingredient = Ingredient.objects.create(name='Soy sauce', recipe=recipe)

        self.assertEqual(str(ingredient), 'Soy sauce')
