# tests/test_core.py

import unittest
from sunny_order_splitter.binance_umfutures import UMFuturesOrderSplitter

class TestUMFuturesOrderSplitter(unittest.TestCase):
    def test_split_order(self):
        production = False # Set to True for production
        
        api_key = "63551008d09ed3a1d619644fbef3b27469b9518f0218c83e499843973e703146"
        secret_key = "ae8a0dd6278350d19d796ceade26e7acf552b64178398a1dd9fb8f7191ccbddb"
        symbol = 'BTCUSDT'
        umfos = UMFuturesOrderSplitter(symbol, api_key, secret_key, production)
        
        # Call split_order method with test parameters
        
        params = {
            "side": "SELL", # "BUY" or "SELL""
            "orderAmount": 2000,
            #"totalAmount": 200,
            "percentTotalAmount": 100,
            "leverage": 2, # 开仓杠杆 最大5倍
            "interval": 2
        }

        
        
        result = umfos.split_order(params)
        if result:
            print(f"Orders placed successfully: {result['num_orders_success']} out of {result['num_orders']}")
            print(f"Total quantity bought: {result['quantity']}")
        else:
            print("Failed to place orders.")
        
        """
        results_close_order = umfos.close_position()
        if results_close_order:
            print(f"Order closed successfully:{results_close_order['symbol']} {results_close_order['quantity']}")
        else:
            print("Failed to close order.")
        """


if __name__ == "__main__":
    unittest.main()
