import unittest
import os
from main import Product, ProductManager

class TestProduct(unittest.TestCase):

    def setUp(self):
        self.manager = ProductManager()

    # 1
    def test_create_product(self):
        p = self.manager.create("Хлеб", 50.0, 10)
        self.assertEqual(p.name, "Хлеб")
        self.assertEqual(p.price, 50.0)
        self.assertEqual(p.quantity, 10)
        self.assertEqual(len(self.manager.products), 1)

    # 2
    def test_create_negative_price(self):
        with self.assertRaises(ValueError):
            self.manager.create("Хлеб", -10, 5)

    # 3
    def test_create_negative_quantity(self):
        with self.assertRaises(ValueError):
            self.manager.create("Хлеб", 50, -5)

    # 4
    def test_total_cost(self):
        p = Product("Молоко", 80.0, 3)
        self.assertEqual(p.total_cost(), 240.0)

    # 5
    def test_update_product(self):
        self.manager.create("Хлеб", 50.0, 10)
        self.manager.update(0, price=60.0)
        self.assertEqual(self.manager.read_by_index(0).price, 60.0)

    # 6
    def test_update_invalid_index(self):
        with self.assertRaises(IndexError):
            self.manager.update(5, name="Test")

    # 7
    def test_delete_product(self):
        self.manager.create("Хлеб", 50.0, 10)
        self.manager.create("Молоко", 80.0, 5)
        removed = self.manager.delete(0)
        self.assertEqual(removed.name, "Хлеб")
        self.assertEqual(len(self.manager.products), 1)

    # 8
    def test_delete_invalid_index(self):
        with self.assertRaises(IndexError):
            self.manager.delete(3)

    # 9
    def test_save_and_load(self):
        self.manager.create("Хлеб", 50.0, 10)
        self.manager.create("Молоко", 80.0, 5)
        filename = "test_products.json"
        self.manager.save_to_file(filename)
        new_manager = ProductManager()
        new_manager.load_from_file(filename)
        self.assertEqual(len(new_manager.products), 2)
        self.assertEqual(new_manager.products[0].name, "Хлеб")
        os.remove(filename)

    # 10
    def test_report_total(self):
        self.manager.create("Хлеб", 50.0, 10)
        self.manager.create("Молоко", 80.0, 5)
        cost, qty = self.manager.report_total()
        self.assertEqual(cost, 500.0 + 400.0)
        self.assertEqual(qty, 15)

    # 11
    def test_report_most_expensive(self):
        self.manager.create("Хлеб", 50.0, 10)
        self.manager.create("Молоко", 80.0, 5)
        expensive = self.manager.report_most_expensive()
        self.assertEqual(expensive.name, "Молоко")
        self.assertEqual(expensive.price, 80.0)

if __name__ == "__main__":
    unittest.main()