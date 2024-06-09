import logging
import math
import time
from binance.spot import Spot as Client
from binance.lib.utils import config_logging
from binance.error import ClientError

config_logging(logging, logging.INFO)

class SpotOrderSplitter:

    BASE_URL = 'https://api.binance.com'
    TESTNET_BASE_URL = 'https://testnet.binance.vision'

    def __init__(self, symbol, api_key, secret_key, production=True):
        base_url = self.BASE_URL if production else self.TESTNET_BASE_URL
        self.client = Client(api_key, secret_key, base_url=base_url)
        self.symbol = symbol
        self.production = production
        self._initialize_symbol_info()

    def _initialize_symbol_info(self):
        """
        初始化交易对信息
        """
        response = self.get_exchange_info(self.symbol)
        if response:
            symbol_info = response['symbols'][0]
            self.baseAsset = symbol_info['baseAsset']
            self.quoteAsset = symbol_info['quoteAsset']
            self.filters = symbol_info['filters']
        else:
            raise ValueError(f"Failed to get exchange info for symbol: {self.symbol}")

    def get_exchange_info(self, symbol):
        """
        获取交易币对相关信息
        """
        try:
            return self.client.exchange_info(symbol)
        except ClientError as error:
            self._log_error(error)
        return None

    def place_order(self, params):
        """
        在 Binance 下单
        """
        try:
            response = self.client.new_order(**params)
            logging.info(f"Order placed: {response}")
            return response
        except ClientError as error:
            self._log_error(error)
        return False

    def split_order(self, params):
        """
        将总金额拆分成多笔订单并按指定间隔下单
        """
        self._validate_params(params)

        side = params['side']
        order_amount = params['orderAmount']
        interval = params['interval']

        total_amount = self._calculate_total_amount(params, side)
        logging.info(f"Total amount: {total_amount}")

        num_orders = math.ceil(total_amount / order_amount)
        quantity, num_orders_success = 0, 0

        for i in range(num_orders):
            current_order_amount = self._calculate_order_amount(i, num_orders, order_amount, total_amount)
            logging.info(f"Order {i + 1} amount: {current_order_amount}")
            
            current_order_params = self._create_order_params(side, current_order_amount)
            response = self.place_order(current_order_params)
            
            if response:
                quantity += float(response['executedQty'])
                num_orders_success += 1
            else:
                logging.error(f"Order {i + 1} failed.")
                break

            if i < num_orders - 1:
                time.sleep(interval)

        return {
            "symbol": self.symbol,
            "quantity": quantity,
            "num_orders_success": num_orders_success,
            "num_orders": num_orders
        }

    def _validate_params(self, params):
        """
        验证参数
        """
        required_params = ['side', 'orderAmount', 'interval']
        for param in required_params:
            if param not in params:
                raise ValueError(f"Missing required parameter: {param}")

        side = params['side']
        if side not in ['BUY', 'SELL']:
            raise ValueError("The 'side' parameter must be either 'BUY' or 'SELL'.")

        if 'totalAmount' not in params and 'percentTotalAmount' not in params:
            raise ValueError("Either 'totalAmount' or 'percentTotalAmount' must be provided.")

    def _calculate_total_amount(self, params, side):
        """
        计算总金额
        """
        if 'totalAmount' in params:
            return params['totalAmount']
        
        percent_total_amount = params['percentTotalAmount']
        asset_to_check = self.quoteAsset if side == "BUY" else self.baseAsset
        balance = self.get_balance(asset_to_check)
        return balance * percent_total_amount / 100

    def _calculate_order_amount(self, i, num_orders, order_amount, total_amount):
        """
        计算每笔订单的金额
        """
        if i < num_orders - 1:
            return order_amount
        return round(total_amount - order_amount * (num_orders - 1), self.get_precision())

    def _create_order_params(self, side, order_amount):
        """
        创建订单参数
        """
        params = {
            "symbol": self.symbol,
            "side": side,
            "type": "MARKET"
        }

        if side == "BUY":
            params["quoteOrderQty"] = order_amount
        else:
            params["quantity"] = order_amount

        return params

    def get_balance(self, asset):
        """
        获取指定资产的余额
        """
        if self.production:
            try:
                response = self.client.user_asset(asset=asset)
                if response:
                    return float(response[0]['free'])
            except ClientError as error:
                self._log_error(error)
        else:
            return 100.48547854  # 测试环境固定返回值
        return 0

    def get_precision(self):
        """
        获取币对的精度
        """
        for filter in self.filters:
            if filter['filterType'] == 'LOT_SIZE':
                return int(-math.log10(float(filter['stepSize'])))
        return 0

    @staticmethod
    def _log_error(error):
        """
        记录错误日志
        """
        logging.error(
            "Found error. status: {}, error code: {}, error message: {}".format(
                error.status_code, error.error_code, error.error_message
            )
        )
