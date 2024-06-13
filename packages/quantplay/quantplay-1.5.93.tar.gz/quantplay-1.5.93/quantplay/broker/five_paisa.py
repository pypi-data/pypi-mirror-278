import numpy as np
import pandas as pd
import pyotp, pickle, codecs
from py5paisa import FivePaisaClient
from retrying import retry
import json, traceback
from datetime import datetime

from quantplay.broker.generics.broker import Broker
from quantplay.exception.exceptions import (
    RetryableException,
    TokenException,
    QuantplayOrderPlacementException,
    InvalidArgumentException,
    retry_exception,
)
from quantplay.utils.constant import Constants, timeit, OrderStatus

logger = Constants.logger


class FivePaisa(Broker):
    @retry(
        wait_exponential_multiplier=1000,
        wait_exponential_max=10000,
        stop_max_attempt_number=3,
        retry_on_exception=retry_exception,
    )
    @timeit(MetricName="5Paisa:__init__")
    def __init__(
        self,
        app_source=None,
        app_user_id=None,
        app_password=None,
        user_key=None,
        encryption_key=None,
        client_id=None,
        totp_key=None,
        pin=None,
        client=None,
        load_instrument=True,
    ):
        self.broker_name = "FivePaisa_OpenAPI"
        try:
            if client:
                self.set_client(client)
            else:
                client = FivePaisaClient(
                    cred={
                        "APP_SOURCE": app_source,
                        "APP_NAME": f"5P{client_id}",
                        "USER_ID": app_user_id,
                        "USER_KEY": user_key,
                        "PASSWORD": app_password,
                        "ENCRYPTION_KEY": encryption_key,
                    }
                )
                self.user_key = user_key
                self.client = client
                self.client.get_totp_session(client_id, pyotp.TOTP(totp_key).now(), pin)

                try:
                    self.margins()
                except TokenException as e:
                    raise RetryableException("Generating token again")
        except RetryableException as e:
            raise
        except Exception as e:
            raise e

        self.set_user_id()

        if load_instrument:
            self.load_instrument()
        super(FivePaisa, self).__init__()

    def set_client(self, serialized_client):
        self.client = pickle.loads(codecs.decode(serialized_client.encode(), "base64"))

    def set_user_id(self):
        self.user_id = self.client.client_code

    def get_client(self):
        return codecs.encode(pickle.dumps(self.client), "base64").decode()

    def load_instrument(self):
        super().load_instrument("5paisa_instruments")

    def handle_exception(self, e):
        if "Unauthorized" in e.reason:
            raise TokenException("Token Expired")
        raise RetryableException(e.reason)

    def token_url(self):
        url = f"https://dev-openapi.5paisa.com/WebVendorLogin/VLogin/Index?VendorKey={self.user_key}&ResponseURL=http://127.0.0.1"

    def holdings(self):
        data = self.client.holdings()
        return pd.DataFrame(data)

    def set_access_token(self, access_token):
        self.access_token = access_token

    def get_product(self, product):
        if product == "NRML":
            return "D"
        elif product == "CNC":
            return "D"
        elif product == "MIS":
            return "I"
        return product

    def get_lot_size(self, exchange, tradingsymbol):
        tradingsymbol = self.get_symbol(tradingsymbol, exchange)
        return int(
            self.symbol_data["{}:{}".format(exchange, tradingsymbol)]["lot_size"]
        )

    @retry(
        wait_exponential_multiplier=1000,
        wait_exponential_max=10000,
        stop_max_attempt_number=3,
        retry_on_exception=retry_exception,
    )
    @timeit(MetricName="5Paisa:profile")
    def profile(self):
        response = {"user_id": self.client.client_code}

        return response

    @retry(
        wait_exponential_multiplier=1000,
        wait_exponential_max=10000,
        stop_max_attempt_number=3,
        retry_on_exception=retry_exception,
    )
    @timeit(MetricName="5Paisa:get_ltp")
    def get_ltp(self, exchange, tradingsymbol):
        tradingsymbol = self.get_symbol(tradingsymbol, exchange)
        exchange_name = self.get_exchange(exchange)
        exchange_type = self.get_exchange_type(exchange)
        token = self.symbol_attribute(exchange, tradingsymbol, "token")
        req_list_ = [
            {"Exch": exchange_name, "ExchType": exchange_type, "ScripCode": token}
        ]

        return self.client.fetch_market_feed_scrip(req_list_)["Data"][0]["LastRate"]

        return response

    def add_exchange(self, data):
        exchange_condition = [
            (data["Exch"] == "N") & (data["ExchType"] == "D"),
            (data["Exch"] == "N") & (data["ExchType"] == "C"),
            (data["Exch"] == "B") & (data["ExchType"] == "D"),
            (data["Exch"] == "B") & (data["ExchType"] == "C"),
        ]

        exchange_name = ["NFO", "NSE", "BFO", "BSE"]

        data.loc[:, "exchange"] = np.select(
            exchange_condition, exchange_name, default=0
        )

    @retry(
        wait_exponential_multiplier=3000,
        wait_exponential_max=10000,
        stop_max_attempt_number=3,
        retry_on_exception=retry_exception,
    )
    @timeit(MetricName="5Paisa:holdings")
    def holdings(self):
        holdings = self.client.holdings()
        if holdings is None:
            raise TokenException("5Paisa Token expired")
        if len(holdings) == 0:
            return pd.DataFrame(columns=self.holdings_column_list)
        holdings = pd.DataFrame(holdings)
        holdings.rename(
            columns={
                "Symbol": "tradingsymbol",
                "AvgRate": "average_price",
                "CurrentPrice": "price",
                "NseCode": "token",
                "Quantity": "quantity",
                "DPQty": "pledged_quantity",
                "Exch": "exchange",
            },
            inplace=True,
        )

        holdings["isin"] = None
        holdings["exchange"] = holdings["exchange"].replace(["B", "N"], ["BSE", "NSE"])
        holdings["token"] = np.where(
            holdings.exchange == "BSE", holdings.BseCode, holdings.token
        )
        holdings["buy_value"] = holdings.quantity * holdings.average_price
        holdings["current_value"] = holdings.quantity * holdings.price
        holdings["pct_change"] = (holdings.price / holdings.average_price - 1) * 100
        return holdings[self.holdings_column_list]

    @retry(
        wait_exponential_multiplier=3000,
        wait_exponential_max=10000,
        stop_max_attempt_number=3,
        retry_on_exception=retry_exception,
    )
    @timeit(MetricName="5Paisa:positions")
    def positions(self, drop_cnc=True):
        # create an instance of the API class
        positions = self.client.positions()
        if positions is None:
            raise TokenException("5Paisa Token expired")

        if len(positions) == 0:
            return pd.DataFrame(columns=self.positions_column_list)
        positions = pd.DataFrame(positions)
        positions.rename(
            columns={
                "ScripName": "tradingsymbol",
                "AvgRate": "average_price",
                "SellQty": "sell_quantity",
                "BuyQty": "buy_quantity",
                "SellValue": "sell_value",
                "BuyValue": "buy_value",
                "LTP": "ltp",
                "ScripCode": "token",
                "NetQty": "quantity",
            },
            inplace=True,
        )

        positions["sell_quantity"] = np.where(
            positions.CFQty < 0,
            -positions.CFQty + positions.sell_quantity,
            positions.sell_quantity,
        )
        positions["buy_quantity"] = np.where(
            positions.CFQty > 0,
            positions.CFQty + positions.buy_quantity,
            positions.buy_quantity,
        )
        positions["buy_value"] = (
            positions.buy_value + positions.CFQty * positions.AvgCFQty
        )
        # positions["sell_value"] = positions.BookedPL
        # positions["buy_value"] = 0

        positions.loc[:, "pnl"] = positions.sell_value - positions.buy_value
        positions.loc[:, "pnl"] += (
            positions.buy_quantity - positions.sell_quantity
        ) * positions.ltp

        self.add_exchange(positions)

        positions.loc[:, "option_type"] = np.where(
            positions.exchange.isin(["NFO", "BFO"]),
            positions.tradingsymbol.str.split(" ").str[-2],
            np.nan,
        )

        positions["product"] = positions["OrderFor"].replace(
            ["I", "D"], ["MIS", "NRML"]
        )
        positions["product"] = np.where(
            (
                (positions["exchange"].isin(["NSE", "BSE"]))
                & (positions["product"] == "NRML")
            ),
            "CNC",
            positions["product"],
        )

        if drop_cnc:
            positions = positions[positions["product"] != "CNC"]
        return positions[self.positions_column_list]

    @retry(
        wait_exponential_multiplier=1000,
        wait_exponential_max=10000,
        stop_max_attempt_number=3,
        retry_on_exception=retry_exception,
    )
    @timeit(MetricName="Upstox:orders")
    def orders(self, tag=None, add_ltp=True):
        orders = self.client.order_book()
        if len(orders) == 0:
            return pd.DataFrame(columns=self.orders_column_list)
        orders = pd.DataFrame(orders)
        self.add_exchange(orders)

        orders.rename(
            columns={
                "OrderRequesterCode": "user_id",
                "ExchOrderID": "order_id",
                "ScripCode": "token",
                "ScripName": "tradingsymbol",
                "BuySell": "transaction_type",
                "AveragePrice": "average_price",
                "Qty": "quantity",
                "Rate": "price",
                "SLTriggerRate": "trigger_price",
                "OrderStatus": "status",
                "TradedQty": "filled_quantity",
                "PendingQty": "pending_quantity",
                "BrokerOrderTime": "order_timestamp",
                "Reason": "status_message",
            },
            inplace=True,
        )

        positions = self.positions()
        positions = positions.sort_values("product").groupby(["tradingsymbol"]).head(1)
        orders = pd.merge(
            orders,
            positions[["tradingsymbol", "ltp"]],
            how="left",
            left_on=["tradingsymbol"],
            right_on=["tradingsymbol"],
        )

        orders.loc[:, "order_type"] = np.where(
            orders["AtMarket"] == "Y", "MARKET", "LIMIT"
        )
        orders.loc[:, "order_type"] = np.where(
            ((orders["order_type"] == "LIMIT") & (orders["WithSL"] == "Y")),
            "SL",
            orders["order_type"],
        )

        orders.loc[:, "pnl"] = (
            orders.ltp * orders.filled_quantity
            - orders.average_price * orders.filled_quantity
        )
        orders.loc[:, "pnl"] = np.where(
            orders.transaction_type == "SELL", -orders.pnl, orders.pnl
        )
        orders.transaction_type = orders.transaction_type.replace(
            ["S", "B"], ["SELL", "BUY"]
        )

        if tag:
            orders = orders[orders.tag == tag]

        orders["tradingsymbol"] = np.where(
            orders.exchange == "NSE",
            orders.tradingsymbol.str.replace("-EQ", ""),
            orders.tradingsymbol,
        )

        orders["update_timestamp"] = orders.order_timestamp
        orders["status"] = orders.status.replace(
            ["Pending", "Modified", "Cancelled", "Fully Executed"],
            [
                OrderStatus.open,
                OrderStatus.open,
                OrderStatus.cancelled,
                OrderStatus.complete,
            ],
        )
        orders["status"] = np.where(
            orders.status.str.lower().str.contains("rejected"),
            OrderStatus.rejected,
            orders.status,
        )
        orders["status"] = np.where(
            ((orders.status == "OPEN") & (orders.order_type == "SL")),
            OrderStatus.trigger_pending,
            orders.status,
        )

        orders["product"] = orders["DelvIntra"].replace(["D", "I"], ["CNC", "MIS"])
        orders["product"] = np.where(
            ((orders["product"] == "CNC") & (orders["exchange"].isin(["NFO", "BFO"]))),
            "NRML",
            orders["product"],
        )

        orders["tag"] = None
        orders["status_message_raw"] = None
        orders["variety"] = "regular"
        orders["order_timestamp"] = orders.order_timestamp.apply(
            lambda x: datetime.fromtimestamp(int(x[6:16]))
        )
        orders["update_timestamp"] = orders.update_timestamp.apply(
            lambda x: datetime.fromtimestamp(int(x[6:16]))
        )

        orders = orders[self.orders_column_list]
        return orders

    def get_symbol(self, symbol, exchange=None):
        if symbol not in self.quantplay_symbol_map:
            return symbol
        return self.quantplay_symbol_map[symbol]

    @staticmethod
    def is_intraday(product):
        if product in ["MIS"]:
            return True
        return False

    @staticmethod
    def get_exchange(exch):
        return exch[0]

    @staticmethod
    def get_exchange_type(exchange):
        if exchange in ["NSE", "BSE"]:
            return "C"
        elif exchange in ["NFO", "BFO"]:
            return "D"
        raise InvalidArgumentException(f"exchange {exchange} not supported")

    @timeit(MetricName="FivePaisa:place_order")
    def place_order(
        self,
        tradingsymbol=None,
        exchange=None,
        quantity=None,
        order_type=None,
        transaction_type=None,
        tag=None,
        product=None,
        price=None,
        trigger_price=None,
    ):
        try:
            if trigger_price is None:
                trigger_price = 0

            product = self.get_product(product)
            tradingsymbol = self.get_symbol(tradingsymbol)

            try:
                token = self.symbol_attribute(exchange, tradingsymbol, "token")
            except Exception as e:
                raise InvalidArgumentException(
                    f"Invalid symbol {tradingsymbol} for exchange {exchange}"
                )

            Constants.logger.info(
                f"[PLACING_ORDER] {tradingsymbol} {transaction_type[0]} {exchange} {token} {quantity}"
            )
            response = self.client.place_order(
                OrderType=transaction_type[0],
                Exchange=FivePaisa.get_exchange(exchange),
                ExchangeType=FivePaisa.get_exchange_type(exchange),
                ScripCode=token,
                Qty=quantity,
                Price=price,
                IsIntraday=FivePaisa.is_intraday(product),
                StopLossPrice=trigger_price,
            )

            logger.info(f"[PLACE_ORDER_RESPONSE] {self.broker_name} {response}")
            if response is None:
                raise QuantplayOrderPlacementException(
                    "Failed to place order on 5Paisa"
                )
            if "Status" in response and response["Status"] == 1:
                logger.error(
                    f"[ORDER_PLACED_FAILED] {self.broker_name}-{self.user_id} {response}"
                )
                raise QuantplayOrderPlacementException(response["Message"])
            if "BrokerOrderID" in response:
                return response["BrokerOrderID"]
        except (QuantplayOrderPlacementException, InvalidArgumentException) as e:
            raise e
        except Exception as e:
            traceback.print_exc()
            exception_message = "Order placement failed with error [{}]".format(str(e))
            logger.error(f"[PLACE_ORDER_FAILED] {self.broker_name} {exception_message}")

    @retry(
        wait_exponential_multiplier=3000,
        wait_exponential_max=10000,
        stop_max_attempt_number=3,
        retry_on_exception=retry_exception,
    )
    @timeit(MetricName="FivePaisa:margins")
    def margins(self):
        margins = self.client.margin()
        if margins is None:
            raise TokenException("5Paisa Token expired")
        margins = margins[0]

        margins = {
            "margin_used": margins["MarginUtilized"],
            "margin_available": margins["NetAvailableMargin"],
        }
        return margins

    @timeit(MetricName="5Paisa:account_summary")
    def account_summary(self):
        margins = self.margins()
        response = {
            "margin_used": margins["margin_used"],
            "margin_available": margins["margin_available"],
            "pnl": float(self.positions().pnl.sum()),
        }
        return response

    def get_quantplay_product(self, exchange, product):
        product_map = {"D": "CNC", "I": "MIS"}
        if product in product_map:
            product = product_map[product]
        if product == "CNC" and exchange in ["NFO", "BFO"]:
            product = "NRML"

        return product
