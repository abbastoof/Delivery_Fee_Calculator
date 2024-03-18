from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, field_validator
from . import time_validity
from datetime import datetime
from .calculation import FeeCalculator
import ciso8601

app = FastAPI(title="Calculate Delivery Fee")

class CartItems(BaseModel):
    cart_value: int = Field(..., gt=0)
    delivery_distance: int = Field(..., gt=0)
    number_of_items: int = Field(..., gt=0)
    time: str

    @field_validator("time")
    @classmethod
    def validate_time(cls, value) -> datetime:
        """
        Validates the time value is in ISO 8601 format and performs additional data integrity checks.

        Args:
            value (str): The time value to be validated.

        Returns:
            datetime.datetime: The parsed datetime object if valid.

        Raises:
            HTTPException: If the value is not in ISO 8601 format or fails data integrity checks.
        """
        try:
            datetime_object = ciso8601.parse_datetime(value)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid time format, must be ISO 8601")

        time_validity.check_date_time_validity(datetime_object)
        return datetime_object

@app.post("/calculate_cost/")
async def calculate_delivery_fee(cart_items: CartItems):
    delivery_fee = FeeCalculator.calculate_total_fee(cart_items)
    return JSONResponse(content={"delivery_fee": delivery_fee}, status_code=200)
