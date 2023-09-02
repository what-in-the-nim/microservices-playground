from datetime import datetime
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field


class OrderStatus(str, Enum):
    created = "created"
    confirmed = "confirmed"
    cancelled = "cancelled"
    delivered = "delivered"


class Order(BaseModel):
    id: int
    customer_id: int
    product_ids: List[int]
    status: OrderStatus = OrderStatus.created
    created_at: datetime = datetime.now()

    @classmethod
    def from_tuple(cls, order_tuple):
        return cls(
            id=order_tuple[0],
            customer_id=order_tuple[1],
            product_ids=[int(i) for i in order_tuple[2].split(",")],
            status=order_tuple[3],
            created_at=order_tuple[4],
        )

    @property
    def tuple(self):
        return (
            self.id,
            self.customer_id,
            ",".join([str(item) for item in self.product_ids]),
            self.status,
            self.created_at,
        )
