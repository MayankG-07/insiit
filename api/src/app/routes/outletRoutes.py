from appTypes.outletTypes import FoodOutletDetails, NewFoodOutletBodyParams
from app.app import app
from db import connect, disconnect
from app.outlet.outlet import FoodOutlet
from app.auth.key import get_api_key
from fastapi import Depends, status, HTTPException
from fastapi.security.api_key import APIKey


@app.get("/food-outlet")
async def get_all_food_outlet_details(api_key: APIKey = Depends(get_api_key)):
    con = connect()
    cursor = con.cursor()

    cursor.execute("SELECT id FROM food_outlets")
    result = cursor.fetchall()
    ids = [row[0] for row in result]
    details = []

    for id in ids:
        outlet = FoodOutlet(id=id)
        outlet.sync_details(con)
        details.append(outlet.__dict__)

    disconnect(con)
    return details


@app.get("/food-outlet/{id}")
async def get_food_outlet_details(
    id: int, api_key: APIKey = Depends(get_api_key)
) -> FoodOutletDetails:
    con = connect()

    outlet = FoodOutlet(id=id)
    outlet.sync_details(con)

    disconnect(con)

    return outlet.__dict__


@app.post("/food-outlet", status_code=status.HTTP_201_CREATED)
async def create_food_outlet(
    params: NewFoodOutletBodyParams, api_key: APIKey = Depends(get_api_key)
):
    con = connect()
    outlet = FoodOutlet(**params.model_dump())
    try:
        outlet.sync_details(con)
        disconnect(con)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Food outlet already exists",
        )
    except HTTPException as e:
        if e.status_code != status.HTTP_404_NOT_FOUND:
            raise e

    details = outlet.create(con)

    disconnect(con)
    return details

@app.delete("/food-outlet", status_code=status.HTTP_204_NO_CONTENT)
async def delete_food_outlet(id: int, api_key: APIKey = Depends(get_api_key)):
    con = connect()
    outlet = FoodOutlet(id=id)

    try:
        outlet.sync_details(con)
    except HTTPException as e:
        if e.status_code == status.HTTP_404_NOT_FOUND:
            raise e

    outlet.remove(con)
