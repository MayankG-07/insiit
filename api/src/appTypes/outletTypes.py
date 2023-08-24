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


class FoodOutletMenu:
    List[FoodOutletMenuItem]


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


class LocationDetailsJSON(TypedDict):
    latitude: float
    longitude: float


class RatingDetailsJSON(TypedDict):
    total: float
    count: int


class FoodOutletMenuItemJSON(TypedDict):
    name: str
    price: int
    description: Optional[str]
    rating: Optional[RatingDetailsJSON]
    size: Optional[str]
    cal: Optional[int]
    image: Optional[str]


class FoodOutletDetailsJSON(TypedDict):
    id: int
    name: str
    location: Optional[LocationDetailsJSON]
    landmark: Optional[str]
    open_time: Optional[str]
    close_time: Optional[str]
    rating: Optional[RatingDetailsJSON]
    menu: Optional[List[FoodOutletMenuItemJSON]]
    image: Optional[str]


class FoodOutletDBValues:
    Tuple[
        int,
        str,
        Optional[LocationDetailsJSON],
        Optional[str],
        Optional[time],
        Optional[time],
        Optional[RatingDetailsJSON],
        Optional[FoodOutletMenu],
        Optional[str],
    ]


class NewFoodOutletBodyParams(BaseModel):
    name: str
    location: Optional[LocationDetailsJSON] = None
    landmark: Optional[str] = None
    open_time: Optional[time] = None
    close_time: Optional[time] = None
    rating: Optional[RatingDetailsJSON] = None
    menu: Optional[FoodOutletMenu] = None
    image: Optional[str] = None

    class Config:
        arbitrary_types_allowed = True


class UpdateFoodOutletBodyParams(BaseModel):
    name: Optional[str] = None
    location: Optional[LocationDetailsJSON] = None
    landmark: Optional[str] = None
    open_time: Optional[time] = None
    close_time: Optional[time] = None
    rating: Optional[RatingDetailsJSON] = None
    menu: Optional[FoodOutletMenu] = None
    image: Optional[str] = None

    class Config:
        arbitrary_types_allowed = True


class FilterFoodOutletBodyParams(BaseModel):
    name: Optional[str] = None
    location: Optional[LocationDetailsJSON] = None
    landmark: Optional[str] = None
    current_time: Optional[time] = None
    rating: Optional[int] = None

    class Config:
        arbitrary_types_allowed = True


class GetAllFoodOutletDetailsResponseModel(BaseModel):
    outlets: List[FoodOutletDetailsJSON]

    class Config:
        arbitrary_types_allowed = True


class GetFoodOutletDetailsResponseModel(BaseModel):
    outlet: FoodOutletDetailsJSON

    class Config:
        arbitrary_types_allowed = True


class CreateFoodOutletResponseModel(BaseModel):
    outlet: FoodOutletDetailsJSON

    class Config:
        arbitrary_types_allowed = True


class UpdateFoodOutletResponseModel(BaseModel):
    outlet: FoodOutletDetailsJSON

    class Config:
        arbitrary_types_allowed = True


class FilterFoodOutletDetailsJSON(TypedDict):
    id: int
    name: str
    location: Optional[LocationDetailsJSON]
    landmark: Optional[str]
    open_time: Optional[time]
    close_time: Optional[time]
    rating: Optional[RatingDetailsJSON]
    image: Optional[str]


class FilterFoodOutletsResponseModel(BaseModel):
    outlets: List[FilterFoodOutletDetailsJSON]

    class Config:
        arbitrary_types_allowed = True
