import unittest
from unittest.mock import Mock
import sys
sys.path.insert(0, "../../")
from limit.limit_order_agent import LimitOrderAgent
from trading_framework.execution_client import ExecutionClient, ExecutionException

class LimitOrderAgentTest(unittest.TestCase):
    def executionclient(self):
        self.exec_client = Mock(spec=ExecutionClient)
        self.test_object = LimitOrderAgent(self.exec_client)

    def test_add_order(self):
        self.executionclient()
        self.test_object.add_order('buy', 'IBM', 1000, 100)
        self.assertEqual(len(self.test_object.orders), 1)
        self.assertEqual(self.test_object.orders[0], {'action': 'buy', 'product_id': 'IBM', 'amount': 1000, 'limit': 100})  #testing the orders added or not
    
    def test_add_order_validations(self):
        self.executionclient()
        with self.assertRaises(Exception):
            self.test_object.add_order('', 'IBM', 1000, 100) #testing the exception for validation

    def test_on_price_tick_for_buy(self):
        self.executionclient()
        self.test_object.add_order('buy', 'IBM', 1000, 100)
        self.test_object.on_price_tick('IBM', 50)
        self.assertEqual(len(self.test_object.orders), 0)  #testing the price tick for buy flag

    def test_on_price_tick_for_sell(self):
        self.executionclient()
        self.test_object.add_order('sell', 'IBM', 1000, 100)
        self.test_object.on_price_tick('IBM', 1100)
        self.assertEqual(len(self.test_object.orders), 0)  #testing the price tick for sell flag



    

if __name__ == '__main__':
    unittest.main()

    



if __name__=="__main__":
    test = LimitOrderAgent()
    print(test.add_order(True,'d1',20000,2000))
    print(test.add_order(False,'d2',12.12,12.12))
    print(test.add_order(True,'d3',12111,12.12))
    print(test.orders)
    test.on_price_tick("d2", 13)
    test.on_price_tick("d1", 1000)
