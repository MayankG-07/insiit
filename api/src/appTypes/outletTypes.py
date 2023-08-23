from typing import List, Optional
from typing_extensions import TypedDict
from appTypes.globalTypes import Rating, Location
from datetime import time
from pydantic import BaseModel


class FoodOutletMenuItem(TypedDict):
    name: str
    price: int
    description: Optional[str]
    rating: Optional[Rating]
    size: Optional[str]
    cal: Optional[int]
    image: Optional[str]


FoodOutletMenu = List[FoodOutletMenuItem]


class FoodOutletDetails(TypedDict):
    id: int
    name: str
    location: Optional[Location]
    landmark: Optional[str]
    open_time: Optional[time]
    close_time: Optional[time]
    rating: Optional[Rating]
    menu: Optional[FoodOutletMenu]
    image: Optional[str]


class NewFoodOutletBodyParams(BaseModel):
    name: str
    location: Optional[Location] = None
    landmark: Optional[str] = None
    open_time: Optional[time] = None
    close_time: Optional[time] = None
    rating: Optional[Rating] = None
    menu: Optional[FoodOutletMenu] = None
    image: Optional[str] = None
