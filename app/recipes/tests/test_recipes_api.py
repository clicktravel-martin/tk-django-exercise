from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from core.models import Recipe, Ingredient

# Recipes collection resource URL, i.e. /recipes/
RECIPES_URL = reverse('recipes:recipe-list')


def recipe_url(recipe_id):
    """Return recipe resource URL, i.e. /recipes/{recipe_id}/"""
    return reverse('recipes:recipe-detail', args=[recipe_id])


def create_sample_recipe(name, ingredient_names, description=''):
    recipe = Recipe.objects.create(
        name=name,
        description=description,
    )
    for ingredient_name in ingredient_names:
        Ingredient.objects.create(
            name=ingredient_name,
            recipe=recipe
        )
    return recipe


class RecipeApiTests(TestCase):
    """Test suite for recipes API endpoints"""

    def setUp(self):
        self.client = APIClient()

    def test_create_recipe_with_description(self):
        """POST /recipes/ should create recipe and return new resource
            representation, including ID"""
        payload = {
            'name': 'Lemon cheesecake',
            'description': 'Cheesecake (feat. lemon)',
            'ingredients': [
                {'name': 'Lemon'},
                {'name': 'Cheese'}
            ]
        }

        response = self.client.post(RECIPES_URL, payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json(), {
            'id': response.data['id'],
            'name': 'Lemon cheesecake',
            'description': 'Cheesecake (feat. lemon)',
            'ingredients': [
                {'name': 'Lemon'},
                {'name': 'Cheese'}
            ]
        })
        created_recipe = Recipe.objects.get(id=response.data['id'])
        self.assertEqual(created_recipe.name, 'Lemon cheesecake')
        self.assertEqual(created_recipe.description,
                         'Cheesecake (feat. lemon)')
        created_ingredients = Ingredient.objects.filter(recipe=created_recipe)
        self.assertEqual(created_ingredients.count(), 2)
        self.assertEqual(created_ingredients[0].name, 'Lemon')
        self.assertEqual(created_ingredients[1].name, 'Cheese')

    def test_create_recipe_without_description(self):
        """POST /recipes/ should create recipe and return new resource
            representation, including ID"""
        payload = {
            'name': 'Omelette',
            'description': '',
            'ingredients': [
                {'name': 'Egg'},
                {'name': 'Milk'},
                {'name': 'Butter'},
            ]
        }

        response = self.client.post(RECIPES_URL, payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json(), {
            'id': response.data['id'],
            'name': 'Omelette',
            'description': '',
            'ingredients': [
                {'name': 'Egg'},
                {'name': 'Milk'},
                {'name': 'Butter'},
            ]
        })
        created_recipe = Recipe.objects.get(id=response.data['id'])
        self.assertEqual(created_recipe.name, 'Omelette')
        created_ingredients = Ingredient.objects.filter(recipe=created_recipe)
        self.assertEqual(created_ingredients.count(), 3)
        self.assertEqual(created_ingredients[0].name, 'Egg')
        self.assertEqual(created_ingredients[1].name, 'Milk')
        self.assertEqual(created_ingredients[2].name, 'Butter')

    def test_create_recipe_invalid(self):
        """POST /recipes/ with invalid data should return 400"""
        payload = {
            'type': 'Horse',
            'legs': '4',
            'speeds': ['TROT', 'CANTER', 'GALLOP']
        }

        response = self.client.post(RECIPES_URL, payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_read_recipes(self):
        """GET /recipes/ should return all recipes"""
        recipe_1_id = create_sample_recipe(
            'Cheese sandwich',
            ['Bread', 'Cheese'],
            'Bread on the outside, cheese in the middle',
        ).id
        recipe_2_id = create_sample_recipe(
            'Just an apple',
            ['Apple']
        ).id

        response = self.client.get(RECIPES_URL)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), [
            {
                'id': recipe_1_id,
                'name': 'Cheese sandwich',
                'description': 'Bread on the outside, cheese in the middle',
                'ingredients': [
                    {'name': 'Bread'},
                    {'name': 'Cheese'},
                ]
            },
            {
                'id': recipe_2_id,
                'name': 'Just an apple',
                'description': '',
                'ingredients': [
                    {'name': 'Apple'}
                ]
            }
        ])

    def test_read_recipes_with_name_filter(self):
        """GET /recipes/?name={name} should return all recipes whose name
            partially matches the name param"""
        sandwich_1_id = create_sample_recipe(
            'Cheese sandwich',
            ['Bread', 'Cheese', 'Butter'],
            'Bread on the outside, cheese in the middle',
        ).id
        sandwich_2_id = create_sample_recipe(
            'Bread sandwich',
            ['Bread']
        ).id
        create_sample_recipe(
            'Garlic bread',
            ['Bread', 'Garlic', 'Butter']
        )

        response = self.client.get(RECIPES_URL, {'name': 'sand'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), [
            {
                'id': sandwich_1_id,
                'name': 'Cheese sandwich',
                'description': 'Bread on the outside, cheese in the middle',
                'ingredients': [
                    {'name': 'Bread'},
                    {'name': 'Cheese'},
                    {'name': 'Butter'},
                ]
            },
            {
                'id': sandwich_2_id,
                'name': 'Bread sandwich',
                'description': '',
                'ingredients': [{'name': 'Bread'}]
            },
        ])

    def test_read_recipe(self):
        """GET /recipes/{recipe_id} should return the specified recipe"""
        recipe_id = create_sample_recipe(
            'Cheese sandwich',
            ['Bread', 'Cheese', 'Butter'],
            'Bread on the outside, cheese in the middle',
        ).id

        response = self.client.get(recipe_url(recipe_id))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {
            'id': recipe_id,
            'name': 'Cheese sandwich',
            'description': 'Bread on the outside, cheese in the middle',
            'ingredients': [
                {'name': 'Bread'},
                {'name': 'Cheese'},
                {'name': 'Butter'},
            ]
        })

    def test_partially_update_recipe(self):
        """PATCH /recipes/{recipe_id} should update the provided fields of the
            specified recipe"""
        recipe_id = create_sample_recipe(
            'Cheese sandwich',
            ['Bread', 'Cheese', 'Butter'],
            'Bread on the outside, cheese in the middle',
        ).id

        payload = {
            'description': 'The 2nd-most boring sandwich',
            'ingredients': [
                {'name': 'Bread'},
                {'name': 'Cheese'},
            ]
        }
        response = self.client.patch(recipe_url(recipe_id), payload,
                                     format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {
            'id': recipe_id,
            'name': 'Cheese sandwich',
            'description': 'The 2nd-most boring sandwich',
            'ingredients': [
                {'name': 'Bread'},
                {'name': 'Cheese'},
            ]
        })
        updated_recipe = Recipe.objects.get(id=recipe_id)
        self.assertEqual(updated_recipe.description,
                         'The 2nd-most boring sandwich')
        updated_ingredients = Ingredient.objects.filter(recipe=updated_recipe)
        self.assertEqual(updated_ingredients.count(), 2)
        self.assertEqual(updated_ingredients[0].name, 'Bread')
        self.assertEqual(updated_ingredients[1].name, 'Cheese')

    def test_delete_recipe(self):
        """DELETE /recipes/{recipe_id} should delete the specified recipe"""
        recipe_id = create_sample_recipe(
            'Chilli dog',
            ['Hot dog', 'Bun', 'Chilli con carne']
        ).id

        response = self.client.delete(recipe_url(recipe_id))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        with self.assertRaises(Recipe.DoesNotExist):
            Recipe.objects.get(id=recipe_id)
