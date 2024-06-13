from configparser import ConfigParser
from fubon_neo.sdk import FubonSDK, Order
from fubon_neo.constant import TimeInForce, OrderType, PriceType, MarketType, BSAction

from finlab.online.base_account import Account, Stock, Order
from finlab.online.enums import *
from finlab.online.order_executor import calculate_price_with_extra_bid, Position
from finlab import data

from threading import Thread
from decimal import Decimal
import numpy as np
import requests
import datetime
import logging
import math
import copy
import time
import os


class FugleAccount(Account):

    required_module = 'fugle_trade'
    module_version = '0.4.0'

    def __init__(self, *args, **kwargs, account_id:int=0):

        self.check_version()
        self.market = 'tw_stock'
        self.trades = {}
        self.is_realtime = False
        self.timestamp_for_get_position = datetime.datetime.now()


        login_arguments = ['FUBON_PERSON_ID', 'FUBON_PASWWORD', 'FUBON_CERT_PATH', 'FUBON_CERT_PASS']
        functional_argument_names = ['personal_id', 'password', 'cert_path', 'cert_pass']

        login_params = {}

        # check args
        if len(args) == len(login_arguments):
            login_params = {fname: arg for fname, arg in zip(functional_argument_names, args)}

        # check env var
        for fname, name in zip(functional_argument_names, login_arguments):
            if name in os.environ:
                login_params[fname] = os.environ[name]

        # check kwargs
        for fname in functional_argument_names:
            if fname in kwargs:
                login_params[fname] = kwargs[fname]

        #載入設定檔與登入
        self.sdk = FubonSDK()
        self.accounts = self.sdk.login(args)
        self.account = self.accounts.data[account_id]
        self.account_id = account_id

    def create_order(self, action, stock_id, quantity, price=None, odd_lot=False, best_price_limit=False, market_order=False, order_cond=OrderCondition.CASH):

        if quantity <= 0:
            raise ValueError("quantity should be larger than zero")

        bs_action = BSAction.Buy if action == Action.BUY else BSAction.Sell

        price_type = PriceType.Limit if price else PriceType.Flat

        if market_order:
            price = None
            if action == Action.BUY:
                price_type = PriceType.LimitUp
            elif action == Action.SELL:
                price_type = PriceType.LimitDown

        elif best_price_limit:
            price = None
            if action == Action.BUY:
                price_type = PriceType.LimitDown
            elif action == Action.SELL:
                price_type = PriceType.LimitUp


        order_cond = {
            OrderCondition.CASH: Trade.Stock,
            OrderCondition.MARGIN_TRADING: Trade.Margin,
            OrderCondition.SHORT_SELLING: Trade.Short,
            OrderCondition.DAY_TRADING_LONG: Trade.DayTrade,
            OrderCondition.DAY_TRADING_SHORT: Trade.DayTrade,
        }[order_cond]

        ap_code = APCode.IntradayOdd if odd_lot else APCode.Common
        now = datetime.datetime.utcnow() + datetime.timedelta(hours=8)
        if datetime.time(13, 40) < datetime.time(now.hour, now.minute) and datetime.time(now.hour, now.minute) < datetime.time(14, 30) and odd_lot:
            ap_code = APCode.Odd
        if datetime.time(14, 00) < datetime.time(now.hour, now.minute) and datetime.time(now.hour, now.minute) < datetime.time(14, 30) and not odd_lot:
            ap_code = APCode.AfterMarket
            price_flag = PriceType.Limit

        params = dict(
            buy_sell=bs_action,
            stock_no=stock_id,
            quantity=int(quantity*1000),
            ap_code=ap_code,
            price_type=price_type,
            order_type=order_cond,
            price=price,
            time_in_force= TimeInForce.ROD,
            user_def='FiNlAB',
        )

        order = OrderObject(**params)

        try:
            ret = self.sdk.place_order(order)
        except Exception as e:
            logging.warning(
                f"create_order: Cannot create order of {params}: {e}")
            return

        ord_no = ret['ord_no']
        if ord_no == '':
            ord_no = ret['pre_ord_no']
        self.trades[ord_no] = ret
        return ord_no

    def update_order(self, order_id, price=None):

        if isinstance(price, int):
            price = float(price)

        if order_id not in self.trades:
            self.get_orders()

        if order_id not in self.trades:
            logging.warning(
                f"update_order: Order id {order_id} not found, cannot update the price.")

        if price is not None:
            try:
                # IntradayOdd
                if self.trades[order_id].org_order['market_type'] == MarketType.IntradayOdd:
                    fubon_order = self.trades[order_id].org_order
                    action = Action.BUY if fubon_order['buy_sell'] == 'B' else Action.SELL
                    stock_id = fubon_order['stock_no']
                    q = fubon_order['after_qty'] - fubon_order['filled_qty']

                    self.cancel_order(order_id)
                    self.create_order(
                        action=action, stock_id=stock_id, quantity=q, price=price, odd_lot=True)
                else:
                    self.sdk.modify_price(
                        self.trades[order_id].org_order, price)
            except ValueError as ve:
                logging.warning(
                    f"update_order: Cannot update price of order {order_id}: {ve}")


    def cancel_order(self, order_id):
        if not order_id in self.trades:
            self.trades = self.get_orders()

        try:
            self.sdk.cancel_order(self.accounts[0], self.trades[order_id].org_order)
        except Exception as e:
            logging.warning(
                f"cancel_order: Cannot cancel order {order_id}: {e}")

    def get_orders(self):


        success = False
        fetch_count = 0

        while not success:
            try:
                orders = self.sdk.get_order_results()
                success = True
            except:
                logging.warning("get_orders: Cannot get orders, sleep for 1 minute")
                fetch_count += 1
                time.sleep(60)
                if fetch_count > 5:
                    logging.error("get_orders: Cannot get orders, try 5 times, raise error")
                    raise Exception("Cannot get orders")

        ret = {}
        for o in orders:
            order_id = o['order_no']
            if order_id == '':
                raise ValueError("Cannot get order id")

            ret[order_id] = create_finlab_order(o)
        self.trades = ret
        return copy.deepcopy(ret)

    def get_stocks(self, stock_ids):

        if not self.is_realtime:
            self.sdk.init_realtime() # 建立行情連線

        ret = {}
        for s in stock_ids:
            try:
                reststock = self.sdk.marketdata.rest_client.stock
                response = reststock.intraday.quote(symbol='2330')
                ret[s] = to_finlab_stock(response)

            except Exception as e:
                logging.warn(f"Fugle API: cannot get stock {s}")
                logging.warn(e)

        return ret

    def get_position(self):
        order_condition = {
            OrderType.Stock: OrderCondition.CASH,
            OrderType.Margin: OrderCondition.MARGIN_TRADING,
            OrderType.Short: OrderCondition.SHORT_SELLING,
            OrderType.DayTrade: OrderCondition.DAY_TRADING_SHORT,
            # 'A': OrderCondition.DAY_TRADING_SHORT,
        }

        now = datetime.datetime.now()

        total_seconds = (now - self.timestamp_for_get_position).total_seconds()

        if total_seconds < 10:
            time.sleep(10)

        inv = self.sdk.accounting.inventories(self.account).data
        self.timestamp_for_get_position = now

        ret = []
        for i in inv:

            # removed: position of stk_dats is not completed
            # total_qty = sum([int(d['qty']) for d in i['stk_dats']]) / 1000
            total_qty = Decimal(int(i['lastday_qty']) +
                         int(i['buy_filled_qty']) - int(i['sell_filled_qty'])) / 1000

            ii = i['odd']
            total_qty += Decimal(int(ii['lastday_qty']) +
                         int(ii['buy_filled_qty']) - int(ii['sell_filled_qty'])) / 1000

            o = order_condition[i['order_type']]

            if total_qty != 0:
                ret.append({
                    'stock_id': i['stock_no'],
                    'quantity': total_qty if o != OrderCondition.SHORT_SELLING else -total_qty,
                    'order_condition': order_condition[i['trade']]
                })

        return Position.from_list(ret)

    def get_total_balance(self):
        # get bank balance
        bank_balance = self.get_cash()

        # get settlements
        settlements = self.get_settlement()

        # get position balance
        unrealized_pnl = self.sdk.accounting.unrealiezd_gains_and_loses(self.accounts.data[self.account_id])
        account_balance = 0
        for d in unrealized_pnl:
            account_balance += d.cost_price * d.tradable_qty + d.unrealized_profit + d.unrealized_loss

        return bank_balance + settlements + account_balance
    
    def get_cash(self):
        return self.sdk.get_balance()['available_balance']
    
    def get_settlement(self):
        tw_now = datetime.datetime.utcnow() + datetime.timedelta(hours=8)
        settlements = self.sdk.accouting.query_settlement(self.accounts.data[self.account_id],"3d").details
        settlements = sum(int(settlement.total_settlement_amount) for settlement in settlements if datetime.datetime.strptime(
            settlement.settlement_date + ' 10:00', '%Y%m%d %H:%M') > tw_now)
        return settlements

    def support_day_trade_condition(self):
        return True

    def on_trades(self, func):

        order_condition = {
            '0': OrderCondition.CASH,
            '3': OrderCondition.MARGIN_TRADING,
            '4': OrderCondition.SHORT_SELLING,
            '9': OrderCondition.DAY_TRADING_LONG,
            'A': OrderCondition.DAY_TRADING_SHORT,
        }

        @self.acc.sdk.on('dealt')
        def on_dealt(data):
            if isinstance(data, dict):
                time = (datetime.datetime.strptime(f"{str((datetime.datetime.utcnow()+datetime.timedelta(hours=8)).date())} {data['mat_time']}", "%Y-%m-%d %H%M%S%f")-datetime.timedelta(
                    hours=8)).replace(tzinfo=datetime.timezone(datetime.timedelta(hours=8))).isoformat()

                o = Order(order_id=data['ord_no'], stock_id=data['stock_no'],
                          action='BUY' if data['buy_sell'] == 'B' else 'SELL', price=data['mat_price'],
                          quantity=data['mat_qty'], filled_quantity=data['mat_qty'],
                          status='FILLED', order_condition=order_condition[data['trade']],
                          time=time, org_order=None)

                func(o)
        self.threading = Thread(target=lambda: self.sdk.connect_websocket())

    def sep_odd_lot_order(self):
        return True

    def get_price_info(self):
        ref = data.get('reference_price')
        return ref.set_index('stock_id').to_dict(orient='index')


def create_finlab_order(order):
    """將 fugle package 的委託單轉換成 finlab 格式"""

    status = OrderStatus.NEW
    if order['status'] == 50:
        status = OrderStatus.FILLED
    elif order['function_type'] == 0 and order['filled_qty'] == 0:
        status = OrderStatus.NEW
    elif order['filled_qty'] != order['after_qty'] and order['filled_qty'] > 0:
        status = OrderStatus.PARTIALLY_FILLED
    elif order['function_type'] == 30:
        status = OrderStatus.CANCEL

    order_condition = {
        OrderType.Stock: OrderCondition.CASH,
        OrderType.Margin: OrderCondition.MARGIN_TRADING,
        OrderType.Short: OrderCondition.SHORT_SELLING,
        OrderType.DayTrade: OrderCondition.DAY_TRADING_SHORT,
        # 'A': OrderCondition.DAY_TRADING_SHORT,
    }[order['order_type']]

    filled_quantity = order['filled_qty']

    order_id = order['order_no']
    if order_id == '':
        raise ValueError("Cannot get order id")

    return Order(**{
        'order_id': order_id,
        'stock_id': order['stock_no'],
        'action': Action.BUY if order['buy_sell'] == 'B' else Action.SELL,
        'price': order.get('od_price', order['avg_price']),
        'quantity': order['org_qty'],
        'filled_quantity': filled_quantity,
        'status': status,
        'order_condition': order_condition,
        'time': datetime.datetime.strptime(order['date'] + order['last_time'], '%Y%m%d%H%M%S%f'),
        'org_order': order
    })


def to_finlab_stock(json_response):
    """將 fubon 股價行情轉換成 finlab 格式"""
    r = json_response

    if 'statusCode' in r:
        raise Exception('Cannot parse fugle quote data' + str(r))

    if 'bids' in r:
        bids = r['bids']
        asks = r['asks']
    else:
        bids = []
        asks = []

    has_volume = 'lastTrade' in r
    return Stock(
        stock_id=r['symbol'],
        high=r['highPrice'] if has_volume else np.nan,
        low=r['lowPrice'] if has_volume else np.nan,
        close=r['closePrice'] if has_volume else r['previousClose'],
        open=r['openPrice'] if has_volume else np.nan,
        bid_price=bids[0]['price'] if bids else np.nan,
        ask_price=asks[0]['price'] if asks else np.nan,
        bid_volume=bids[0]['size'] if bids else 0,
        ask_volume=asks[0]['size'] if asks else 0,
    )

