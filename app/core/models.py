from django.db import models


class Recipe(models.Model):
    """A recipe with name, optional description and optional to-many
        "ingredients" relationship"""
    name = models.TextField()
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """An ingredient that exists as part of a recipe"""
    name = models.TextField()
    recipe = models.ForeignKey(
        'Recipe',
        on_delete=models.CASCADE,
        related_name='ingredients',
    )

    def __str__(self):
        return self.name
