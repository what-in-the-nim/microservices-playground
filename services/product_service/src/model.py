from datetime import datetime
from typing import Any, Optional, Tuple

from pydantic import BaseModel, Field


class Product(BaseModel):
    id: int
    name: str
    price: float
    quantity: int
    description: Optional[str] = None
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()

    @classmethod
    def from_tuple(cls, product_tuple: Tuple[Any]) -> "Product":
        print(product_tuple)
        return cls(
            id=product_tuple[0],
            name=product_tuple[1],
            price=float(product_tuple[2]),
            quantity=int(product_tuple[3]),
            description=product_tuple[4],
            created_at=product_tuple[5],
            updated_at=product_tuple[6],
        )

    @property
    def tuple(self) -> Tuple[Any]:
        return (
            self.id,
            self.name,
            self.price,
            self.quantity,
            self.description,
            self.created_at,
            self.updated_at,
        )
