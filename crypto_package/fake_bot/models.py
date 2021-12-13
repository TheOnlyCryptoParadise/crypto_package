from typing import List
import pydantic
from datetime import datetime

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