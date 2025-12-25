from dataclasses import dataclass
from typing import List


@dataclass
class TradeItem:
    item: str
    pct: float


@dataclass
class Station:
    id: str
    sistema: str
    estacion: str
    economia: str
    compra: List[TradeItem]
    venta: List[TradeItem]
