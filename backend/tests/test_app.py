import unittest
from app import estimate_days_until_stockout, recommend_stock_action

class TestHeuristics(unittest.TestCase):
    def test_estimate_days_until_stockout(self):
        # Test case with regular demand
        medicine = {"current_stock": 200, "daily_demand": 20}
        self.assertEqual(estimate_days_until_stockout(medicine), 10)
        
        # Test case with zero demand
        medicine = {"current_stock": 200, "daily_demand": 0}
        self.assertEqual(estimate_days_until_stockout(medicine), float('inf'))
        
        # Test case with high demand
        medicine = {"current_stock": 100, "daily_demand": 25}
        self.assertEqual(estimate_days_until_stockout(medicine), 4)

class TestRecommendations(unittest.TestCase):
    def test_recommend_stock_action(self):
        # Test case where stock will run out soon
        medicine = {"current_stock": 50, "daily_demand": 20}
        self.assertEqual(recommend_stock_action(medicine, 3, 200),
                         "Order immediately, stock will run out in 2.5 days.")
        
        # Test case where stock is above storage limit
        medicine = {"current_stock": 300, "daily_demand": 5}
        self.assertEqual(recommend_stock_action(medicine, 3, 200),
                         "Order less frequently due to storage constraints.")
        
        # Test case where stock level is sufficient
        medicine = {"current_stock": 200, "daily_demand": 10}
        self.assertEqual(recommend_stock_action(medicine, 3, 200),
                         "Stock level is sufficient for now.")

if __name__ == '__main__':
    unittest.main()
