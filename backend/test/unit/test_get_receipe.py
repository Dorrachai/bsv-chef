import pytest
from src.static.diets import Diet
from src.util.calculator import calculate_readiness
from src.controllers.controller import ReceipeController
from src.util.dao import DAO

class TestReceipeController(pytest.TestCase):
    def setUp(self):
        self.receipeController = ReceipeController(DAO()) 

    @pytest.mark.unit
    def test_get_receipe_readiness(self):
        # Test case 1: recipe is compatible with diet, readiness is above 0.1
        receipe = {'name': 'Vegan Soup', 'diets': ['vegan'], 'ingredients': {"Carrot": 2, "Broccoli": 1}}
        available_items = {"Carrot": 2, "Broccoli": 1, "Chicken": 2}
        diet = Diet.VEGAN
        self.assertEqual(self.receipeController.get_receipe_readiness(receipe, available_items, diet), 1.0)

        # Test case 2: recipe is not compatible with diet, regardless of readiness
        receipe = {'name': 'Vegan Soup', 'diets': ['vegan'], 'ingredients': {"Carrot": 2, "Broccoli": 1}}
        available_items = {"Carrot": 2, "Broccoli": 1, "Chicken": 2}
        diet = Diet.MEDITERRANEAN
        self.assertEqual(self.receipeController.get_receipe_readiness(receipe, available_items, diet), None)

        # Test case 3: recipe is compatible with diet, readiness is below 0.1
        receipe = {'name': 'Vegan Soup', 'diets': ['vegan'], 'ingredients': {"Carrot": 2, "Broccoli": 1}}
        available_items = {"Carrot": 0, "Broccoli": 0, "Chicken": 2}
        diet = Diet.VEGAN
        self.assertEqual(self.receipeController.get_receipe_readiness(receipe, available_items, diet), None)

        # Test case 4: recipe is compatible with diet, readiness is exactly 0.1
        receipe = {'name': 'Vegan Soup', 'diets': ['vegan'], 'ingredients': {"Carrot": 2, "Broccoli": 1}}
        available_items = {"Carrot": 1, "Broccoli": 0, "Chicken": 2}
        diet = Diet.VEGAN
        self.assertAlmostEqual(self.receipeController.get_receipe_readiness(receipe, available_items, diet), 0.33, places=2)
