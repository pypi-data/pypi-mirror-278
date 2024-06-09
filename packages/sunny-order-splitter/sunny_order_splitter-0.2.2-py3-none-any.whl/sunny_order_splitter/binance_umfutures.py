import logging
import math
import time
from binance.um_futures import UMFutures
from binance.lib.utils import config_logging
from binance.error import ClientError

config_logging(logging, logging.INFO)

class UMFuturesOrderSplitter:
    BASE_URL = 'https://fapi.binance.com'
    TESTNET_BASE_URL = 'https://testnet.binancefuture.com'

    def __init__(self, symbol, api_key, secret_key, production=True):
        base_url = self.BASE_URL if production else self.TESTNET_BASE_URL
        self.client = UMFutures(api_key, secret_key, base_url=base_url)
        self.symbol = symbol
        self.production = production
        self._initialize_symbol_info()

    def _initialize_symbol_info(self):
        response = self.get_exchange_info()
        if response:
            symbol_info = next((item for item in response['symbols'] if item['symbol'] == self.symbol), None)
            if symbol_info:
                self.baseAsset = symbol_info['baseAsset']
                self.quoteAsset = symbol_info['quoteAsset']
                self.filters = symbol_info['filters']
            else:
                raise ValueError(f"Symbol {self.symbol} not found in exchange info.")
        else:
            raise ValueError(f"Failed to get exchange info for symbol: {self.symbol}")

    def get_exchange_info(self):
        try:
            return self.client.exchange_info()
        except ClientError as error:
            self._log_error(error)
            return None

    def place_order(self, params):
        try:
            response = self.client.new_order(**params)
            logging.info(f"Order placed: {response}")
            return response
        except ClientError as error:
            self._log_error(error)
            return False

    def split_order(self, params):
        self._validate_params(params)

        if self._is_dual_side_position():
            if not self._change_to_one_way_mode():
                logging.error("Failed to change to 'One-way' position mode.")
                return False

        side = params['side']
        self._validate_side(side)

        leverage = params['leverage']
        self._change_leverage(leverage)

        order_amount = params['orderAmount'] * leverage
        interval = params['interval']
        total_amount = self._calculate_total_amount(params, side) * leverage
        logging.info(f"Total amount: {total_amount}")

        num_orders = math.ceil(total_amount / order_amount)
        quantity, num_orders_success = 0, 0

        for i in range(num_orders):
            current_order_amount = self._calculate_order_amount(i, num_orders, order_amount, total_amount)
            logging.info(f"Order {i + 1} amount: {current_order_amount}")

            order_params = {
                "symbol": self.symbol,
                "side": side,
                "type": "MARKET",
                "quantity": self._calculate_quantity(current_order_amount),
            }

            response = self.place_order(order_params)
            if response:
                quantity += float(response['origQty'])
                num_orders_success += 1
            else:
                logging.error(f"Order {i + 1} failed.")
                break

            if i < num_orders - 1:
                time.sleep(interval)
        return {"symbol": self.symbol, "quantity": quantity, "num_orders_success": num_orders_success, "num_orders": num_orders}

    def close_position(self):
        position = self.get_current_position()
        if position:
            current_qty = float(position['positionAmt'])
            if current_qty == 0:
                logging.info("No position to close.")
                return False
            side = 'BUY' if current_qty < 0 else 'SELL'
            
            order_params = {
                "symbol": self.symbol,
                "side": side,
                "type": "MARKET",
                "quantity": abs(current_qty),
            }
            response = self.place_order(order_params)
            if response:
                logging.info(f"Position closed: {response}")
                return {"symbol": self.symbol, "quantity": response['origQty']}
            else:
                logging.error("Failed to close position.")
                return False
        else:
            logging.error("Failed to get position information.")
            return False

    def get_current_position(self):
        try:
            positions = self.client.get_position_risk(symbol=self.symbol)
            return positions[0] if positions else None
        except ClientError as error:
            self._log_error(error)
            return None

    def _calculate_quantity(self, amount):
        #amount *= 0.99  # 考虑手续费
        try:
            ticker_price = self.client.ticker_price(symbol=self.symbol)
            price = float(ticker_price['price'])
            return round(amount / price, self.get_precision())
        except ClientError as error:
            self._log_error(error)
            return 0

    def _change_leverage(self, leverage):
        leverage = min(leverage, 5)
        try:
            response = self.client.change_leverage(symbol=self.symbol, leverage=leverage)
            logging.info(f"Leverage changed: {response}")
            return True
        except ClientError as error:
            self._log_error(error)
            return False

    def _calculate_total_amount(self, params, side):
        if 'percentTotalAmount' in params:
            percent_total_amount = params['percentTotalAmount']
            asset_to_check = self.quoteAsset
            balance = self.get_balance(asset_to_check)
            return balance * percent_total_amount * 0.99 / 100
        else:
            raise ValueError("The 'percentTotalAmount' parameter must be provided.")

    def _calculate_order_amount(self, i, num_orders, order_amount, total_amount):
        if i < num_orders - 1:
            return order_amount
        else:
            return round(total_amount - order_amount * (num_orders - 1), self.get_precision())

    def _validate_params(self, params):
        required_params = ['side', 'orderAmount', 'leverage', 'interval', 'percentTotalAmount']
        for param in required_params:
            if param not in params:
                raise ValueError(f"Missing required parameter: {param}")

    def _validate_side(self, side):
        if side not in ['BUY', 'SELL']:
            raise ValueError("The 'side' parameter must be one of 'BUY', 'SELL'.")

    def _is_dual_side_position(self):
        position_mode = self.client.get_position_mode()
        return position_mode['dualSidePosition'] == 'true'

    def _change_to_one_way_mode(self):
        try:
            self.client.change_position_mode(dualSidePosition='false')
            logging.info("Position mode changed to 'One-way'.")
            return True
        except ClientError as error:
            self._log_error(error)
            return False

    def get_balance(self, asset):
        try:
            response = self.client.balance()
            for asset_balance in response:
                if asset_balance['asset'] == asset:
                    return float(asset_balance['availableBalance'])
        except ClientError as error:
            self._log_error(error)
            return 0

    def _log_error(self, error):
        logging.error(
            "Found error. status: {}, error code: {}, error message: {}".format(
                error.status_code, error.error_code, error.error_message
            )
        )

    def get_precision(self):
        for filter in self.filters:
            if filter['filterType'] == 'LOT_SIZE':
                return int(-math.log10(float(filter['stepSize'])))
        return 0
