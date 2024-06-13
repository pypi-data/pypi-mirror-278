from dataclasses import asdict, dataclass
from pyqqq.brokerage.ebest.simple import EBestSimpleDomesticStock
from pyqqq.brokerage.kis.simple import KISSimpleDomesticStock
from pyqqq.data.domestic import get_ticker_info
from pyqqq.datatypes import *
from pyqqq.utils.api_client import raise_for_status, send_request
from pyqqq.utils.array import find
from pyqqq.utils.logger import get_logger
from typing import Optional, List
import asyncio
import os
import pyqqq.config as c

class TradingTracker:
    """
    거래 내역 추적을 위한 클래스입니다

    주문 이벤트를 수신하여 보유 포지션과 미체결 주문을 관리하고 거래 내역을 기록합니다.

    Args:
        simple_api (EBestSimpleDomesticStock | KISSimpleDomesticStock): 간편 거래 API 객체
        fee_rate (float): 증권사 수수료율 (기본값: 0.015%)
    """

    logger = get_logger("trading_tracker")

    def __init__(
        self,
        simple_api: EBestSimpleDomesticStock | KISSimpleDomesticStock,
        fee_rate: float = 0.00015,  # 뱅키스, LS증권 수수료율 0.015%
    ):
        self.positions: List[StockPosition] = []
        """ 보유 포지션 목록 """
        self.pending_orders: List[OrderEvent] = []
        """ 미체결 주문 목록 """
        self.on_pending_order_update: Optional[callable] = None
        """ 미체결 주문 업데이트 이벤트 callback """
        self.on_position_update: Optional[callable] = None
        """ 포지션 업데이트 이벤트 callback """
        self.task: asyncio.Task = None
        """ 백그라운드로 실행되는 거래 이벤트 모니터링 Task """

        self.simple_api = simple_api
        self.stop_event = asyncio.Event()
        self.account_no = None
        self.fee_rate = fee_rate  # 증권사 수수료율
        self.tax_rate = 0.0018  # KOSPI, KOSDAQ 매도시 거래세율 0.18%

    async def start(self):
        """
        거래 내역 추적을 시작합니다
        """
        if isinstance(self.simple_api, EBestSimpleDomesticStock):
            account_info = self.simple_api.get_account()
            self.account_no = account_info["account_no"]
        elif isinstance(self.simple_api, KISSimpleDomesticStock):
            self.account_no = (
                self.simple_api.account_no + self.simple_api.account_product_code
            )

        self.logger.info(f"Trading tarcker started! Account No: {self.account_no}")

        self.positions = self.simple_api.get_positions()
        position_map = {}
        for position in self.positions:
            position_map[position.asset_code] = position

        pending_orders = self.simple_api.get_pending_orders()

        for order in pending_orders:
            order_event = OrderEvent.with_pending_order(self.account_no, order)
            if order_event.side == OrderSide.SELL:
                p = position_map.get(order.asset_code)
                assert p is not None, f"position not found for {order.asset_code}"
                order_event.average_purchase_price = p.average_purchase_price

            self.pending_orders.append(order_event)

        self.task = asyncio.create_task(self._monitor_trading())

    async def stop(self):
        """
        거래 내역 추적을 중지합니다
        """
        self.stop_event.set()

        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.task)

    async def _monitor_trading(self):
        async for event in self.simple_api.listen_order_event(self.stop_event):
            self._handle_order_event(event)

    def _handle_order_event(
        self,
        event: OrderEvent,
    ):
        self.logger.info(
            f"handle_order_event: accno={event.account_no} - {event.order_no}({event.org_order_no})\t{event.side}\t{event.asset_code}\t{event.filled_quantity}/{event.quantity}\t{event.status}"
        )

        if event.account_no != self.account_no:
            return

        prev_order = find(lambda x: x.order_no == event.order_no, self.pending_orders)
        org_order = find(
            lambda x: x.order_no == event.org_order_no, self.pending_orders
        )

        self.logger.info(f"prev_order={'exists' if prev_order else 'not exists'}")

        if event.status == "accepted":
            if event.side == OrderSide.SELL:
                p = find(lambda x: x.asset_code == event.asset_code, self.positions)
                event.average_purchase_price = p.average_purchase_price

            self.pending_orders.append(event)

            if event.org_order_no is not None:
                if org_order is not None:
                    if org_order.quantity == event.quantity:
                        self.pending_orders.remove(org_order)
                    else:
                        org_order.quantity -= event.quantity

            self._notify_pending_order_update()

        elif event.status == "completed" or event.status == "partial":
            if prev_order:
                self.pending_orders.remove(prev_order)

            order_no = event.order_no
            side = event.side
            asset_code = event.asset_code
            quantity = event.quantity
            order_price = event.filled_price
            executed_time = event.filled_time
            tax = 0
            fee = 0
            pnl = None
            pnl_rate = None

            if side == OrderSide.SELL:
                sell_amt = quantity * order_price
                buy_amt = float(quantity * prev_order.average_purchase_price)
                ticker_info = get_ticker_info(asset_code)

                buy_fee = buy_amt * self.fee_rate
                fee = sell_fee = sell_amt * self.fee_rate
                if ticker_info["type"][asset_code] == "EQUITY":
                    tax = sell_tax = sell_amt * self.tax_rate
                else:
                    tax = sell_tax = 0

                pnl = (sell_amt - sell_fee - sell_tax - buy_fee) - buy_amt
                pnl_rate = pnl / buy_amt
            else:
                fee = quantity * order_price * self.fee_rate

            if event.status == "partial":
                if event.side == OrderSide.SELL:
                    event.average_purchase_price = prev_order.average_purchase_price

                self.pending_orders.append(event)

            self._refresh_positions()

            data = TradingHistory(
                date=dtm.date.today().strftime("%Y%m%d"),
                order_no=order_no,
                side="buy" if side == OrderSide.BUY else "sell",
                asset_code=asset_code,
                quantity=quantity,
                order_price=order_price,
                average_purchase_price=(
                    float(prev_order.average_purchase_price)
                    if prev_order.average_purchase_price is not None
                    else None
                ),
                tax=tax,
                fee=fee,
                pnl=pnl,
                pnl_rate=pnl_rate,
                executed_time=(
                    int(executed_time.timestamp() * 1000) if executed_time else None
                ),
                partial=event.status == "partial",
            )

            self._save_trading_history(data)

            self._notify_pending_order_update()
            self._notify_position_update()

        elif event.status == "cancelled":
            if prev_order:
                self.pending_orders.remove(prev_order)

            self._notify_pending_order_update()

    def _refresh_positions(self):
        self.positions = self.simple_api.get_positions()

    def _refresh_pending_orders(self):
        old_pending_orders = {}
        for o in self.pending_orders:
            old_pending_orders[o.order_no] = o

        self.pending_orders = self.simple_api.get_pending_orders()
        for o in self.pending_orders:
            old_pending_order = old_pending_orders.get(o.order_no)
            if old_pending_order is not None:
                o.average_purchase_price = old_pending_order.average_purchase_price

    def _notify_pending_order_update(self):
        if self.on_pending_order_update is not None:
            self.on_pending_order_update()

    def _notify_position_update(self):
        if self.on_position_update is not None:
            self.on_position_update()

    def _save_trading_history(self, history: TradingHistory):
        url = f"{c.PYQQQ_API_URL}/trading-history/{history.order_no}"

        data = asdict(history)
        data["brokerage"] = (
            "ebest" if isinstance(self.simple_api, EBestSimpleDomesticStock) else "kis"
        )
        data["account_no"] = self.account_no

        strategy_name = os.getenv("STRATEGY_NAME")
        if strategy_name is not None:
            data["strategy_name"] = strategy_name

        positions = []
        for p in self.positions:
            d = asdict(p)
            d["average_purchase_price"] = (
                float(d["average_purchase_price"])
                if d["average_purchase_price"] is not None
                else None
            )
            d["current_pnl"] = (
                float(d["current_pnl"]) if d["current_pnl"] is not None else None
            )
            positions.append(d)

        data["positions"] = positions

        r = send_request("POST", url, json=data)
        raise_for_status(r)
