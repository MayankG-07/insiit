from appTypes.outletTypes import (
    NewFoodOutletBodyParams,
    UpdateFoodOutletBodyParams,
    FilterFoodOutletBodyParams,
)
from app.app import app
from app.db import connect, disconnect
from app.interfaces.outlet import FoodOutlet, searchOutlets
from app.interfaces.common import Location, Rating
from app.auth.key import get_api_key
from fastapi import Depends, status, HTTPException
from fastapi.security.api_key import APIKey


@app.get("/food-outlet")
async def get_all_food_outlet_details(
    api_key: APIKey = Depends(get_api_key),
):
    con = connect()
    cursor = con.cursor()

    cursor.execute("SELECT id FROM food_outlets")
    result = cursor.fetchall()
    ids = [row[0] for row in result]
    details = []

    for id in ids:
        outlet = FoodOutlet(id=id)
        await outlet.sync_details(con)
        outlet_details = outlet.__dict__
        outlet_details["location"] = (
            outlet.location.__dict__ if outlet.location is not None else None
        )
        outlet_details["rating"] = (
            outlet.rating.__dict__ if outlet.rating is not None else None
        )
        details.append(outlet_details)

    disconnect(con)
    return {"outlets": details}


@app.get("/food-outlet/{id}")
async def get_food_outlet_details(id: int, api_key: APIKey = Depends(get_api_key)):
    con = connect()

    outlet = FoodOutlet(id=id)
    await outlet.sync_details(con)

    details = outlet.__dict__
    details["location"] = (
        outlet.location.__dict__ if outlet.location is not None else None
    )
    details["rating"] = outlet.rating.__dict__ if outlet.rating is not None else None

    disconnect(con)

    return {"outlet": details}


@app.get("/food-outlet/filter")
async def filter_food_outlets(
    params: FilterFoodOutletBodyParams,
    api_key: APIKey = Depends(get_api_key),
):
    con = connect()
    outlets = await searchOutlets(
        con=con,
        nameFilter=params.name,
        locationFilter=Location(**params.location),
        landmarkFilter=params.landmark,
        timeFilter=params.current_time,
        ratingFilter=params.rating,
    )

    for i in range(len(outlets)):
        outlets[i] = outlets[i].__dict__
        outlets[i]["location"] = outlets[i]["location"].__dict__
        outlets[i]["rating"] = outlets[i]["rating"].__dict__

    return {"outlets": outlets}


@app.post("/food-outlet", status_code=status.HTTP_201_CREATED)
async def create_food_outlet(
    params: NewFoodOutletBodyParams, api_key: APIKey = Depends(get_api_key)
):
    con = connect()
    params_dict = params.model_dump()
    if params_dict["location"] is not None:
        params_dict["location"] = Location(**params_dict["location"])
    if params_dict["rating"] is not None:
        params_dict["rating"] = Rating(**params_dict["rating"])
    outlet = FoodOutlet(**params_dict)
    try:
        await outlet.sync_details(con)
        disconnect(con)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Food outlet already exists",
        )
    except HTTPException as e:
        if e.status_code != status.HTTP_404_NOT_FOUND:
            raise e

    details = await outlet.create(con)

    disconnect(con)
    return {"outlet": details}


@app.put("/food-outlet/{id}")
async def update_food_outlet(
    id: int, params: UpdateFoodOutletBodyParams, api_key: APIKey = Depends(get_api_key)
):
    con = connect()
    outlet = FoodOutlet(id=id)
    await outlet.sync_details(con=con)
    params_dict = params.model_dump()
    for key, value in params_dict.items():
        if value is not None:
            if key == "location":
                outlet.location = Location(**params_dict["location"])
            elif key == "rating":
                outlet.rating = Rating(**params_dict["rating"])
            else:
                outlet.__setattr__(key, value)

    details = await outlet.update(con=con)
    return {"outlet": details}


@app.delete("/food-outlet/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_food_outlet(id: int, api_key: APIKey = Depends(get_api_key)):
    con = connect()
    outlet = FoodOutlet(id=id)

    try:
        await outlet.sync_details(con)
    except HTTPException as e:
        if e.status_code == status.HTTP_404_NOT_FOUND:
            raise e

    await outlet.remove(con)
