from typing import List, Optional, Tuple
from typing_extensions import TypedDict
from app.interfaces.common import Rating, Location
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


class LocationDBValues(TypedDict):
    latitude: float
    longitude: float


class RatingDBValues(TypedDict):
    total: float
    count: int


FoodOutletDBValues: Tuple[
    int,
    str,
    Optional[LocationDBValues],
    Optional[str],
    Optional[time],
    Optional[time],
    Optional[RatingDBValues],
    Optional[FoodOutletMenu],
    Optional[str],
]


class NewFoodOutletBodyParams(BaseModel):
    name: str
    location: Optional[Location] = None
    landmark: Optional[str] = None
    open_time: Optional[time] = None
    close_time: Optional[time] = None
    rating: Optional[Rating] = None
    menu: Optional[FoodOutletMenu] = None
    image: Optional[str] = None


class UpdateFoodOutletBodyParams(BaseModel):
    name: Optional[str] = None
    location: Optional[Location] = None
    landmark: Optional[str] = None
    open_time: Optional[time] = None
    close_time: Optional[time] = None
    rating: Optional[Rating] = None
    menu: Optional[FoodOutletMenu] = None
    image: Optional[str] = None


class FilterFoodOutletBodyParams(BaseModel):
    name: Optional[str] = None
    location: Optional[Location] = None
    landmark: Optional[str] = None
    current_time: Optional[time] = None
    rating: Optional[int] = None


class GetAllFoodOutletDetailsResponseModel(TypedDict):
    outlets: List[FoodOutletDetails]


class GetFoodOutletDetailsResponseModel(TypedDict):
    outlet: FoodOutletDetails


class CreateFoodOutletResponseModel(TypedDict):
    outlet: FoodOutletDetails


class UpdateFoodOutletResponseModel(TypedDict):
    outlet: FoodOutletDetails


class LocationDetails(TypedDict):
    latitude: float
    longitude: float


class RatingDetails(TypedDict):
    total: float
    count: int


class FilterFoodOutletDetails(TypedDict):
    id: int
    name: str
    location: Optional[LocationDetails]
    landmark: Optional[str]
    open_time: Optional[time]
    close_time: Optional[time]
    rating: Optional[RatingDetails]
    image: Optional[str]


class FilterFoodOutletsResponseModel(TypedDict):
    outlets: List[FilterFoodOutletDetails]
