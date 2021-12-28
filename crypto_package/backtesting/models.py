from datetime import datetime
from typing import List, Tuple

import pydantic
from pydantic.main import BaseModel

class Trade(pydantic.BaseModel):
    pair: str
    is_buy: bool
    price: float
    timestamp: datetime
    amount: float


class AnalysisResult(BaseModel):
    trades: List[Trade]
    start_balance: float
    end_balance: float
    start_datetime: datetime
    end_datetime: datetime
    sell_signals: List[Tuple[float, datetime]]
    buy_signals: List[Tuple[float, datetime]]