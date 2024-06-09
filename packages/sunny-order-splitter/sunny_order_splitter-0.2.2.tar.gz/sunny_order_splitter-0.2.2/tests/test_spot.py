# tests/test_core.py

import unittest
from sunny_order_splitter.binance_spot import SpotOrderSplitter

class TestSpotOrderSplitter(unittest.TestCase):
    def test_split_order(self):
        production = False # True正式环境，不传默认True
        
        api_key = "EpcFiKyNEZ6GwpW4w1px60og0SYy0W4A2slX32UeH2hV9FjJfOdKPJDY9NNlbRrB"
        secret_key = "OeIwlnfB0ImKdqTq4n4jLqYxdzYO87Lc8Mr2Z1bbCqraerpomMUJMD7EvtyIFFWh"
        symbol = 'BTCUSDT'
        sos = SpotOrderSplitter(symbol, api_key, secret_key, production)
        
        # Call split_order method with test parameters
        
        params = {
            "side": "BUY",
            "orderAmount": 90,
            #"totalAmount": 100,
            "percentTotalAmount": 80, # 总金额百分比
            "interval": 2
        }
        """
        params = {
            "side": "SELL",
            "orderAmount": 1,
            #"totalAmount": 100,
            "percentTotalAmount":  100,
            "interval": 2
        }
        """
        result = sos.split_order(params)
        if result:
            print(f"Orders placed successfully: {result['num_orders_success']} out of {result['num_orders']}")
            print(f"Total quantity bought: {result['quantity']}")
        else:
            print("Failed to place orders.")
            


if __name__ == "__main__":
    unittest.main()
