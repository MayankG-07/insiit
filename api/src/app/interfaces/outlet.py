from typing import Optional, List
from app.interfaces.common import Location, Rating
from appTypes.outletTypes import FoodOutletMenu, FoodOutletDetails, FoodOutletDBValues
from datetime import time
from fastapi import HTTPException, status
from psycopg2 import connection
import geopy.distance


class FoodOutlet:
    def __init__(
        self,
        id: Optional[int] = None,
        name: Optional[str] = None,
        location: Optional[Location] = None,
        landmark: Optional[str] = None,
        open_time: Optional[time] = None,
        close_time: Optional[time] = None,
        rating: Optional[Rating] = None,
        menu: Optional[FoodOutletMenu] = None,
        image: Optional[str] = None,
    ):
        self.id = id
        self.name = name
        self.location = location
        self.landmark = landmark
        self.open_time = open_time
        self.close_time = close_time
        self.rating = rating
        self.menu = menu
        self.image = image

    async def sync_details(self, con: connection):
        cursor = con.cursor()

        if self.id is not None:
            cursor.execute(f"SELECT * FROM food_outlets WHERE id={self.id}")
        elif self.name is not None:
            cursor.execute(f"SELECT * FROM food_outlets WHERE name='{self.name}'")
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Insufficient data"
            )

        result: List[FoodOutletDBValues] = cursor.fetchone()

        try:
            self.id = result[0]
            self.name = result[1]
            self.location = Location(
                latitude=result[2]["latitude"], longitude=result[2]["longitude"]
            )
            self.landmark = result[3]
            self.open_time = result[4]
            self.close_time = result[5]
            self.rating = Rating(total=result[6]["total"], count=result[6]["count"])
            self.menu = result[7]
            self.image = result[8]
        except TypeError:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Food outlet not found"
            )

    async def create(self, con: connection) -> FoodOutletDetails:
        cursor = con.cursor()

        cursor.execute(
            "INSERT INTO food_outlets(name, location, landmark, open_time, close_time, rating, menu, image) VALUES(%s, %s, %s, %s, %s, %s, %s, %s) RETURNING id",
            (
                self.name,
                {
                    "latitude": self.location.latitude,
                    "longitude": self.location.longitude,
                },
                self.landmark,
                self.open_time,
                self.close_time,
                {"total": self.rating.total, "count": self.rating.count},
                self.menu,
                self.image,
            ),
        )

        self.id = cursor.fetchone()[0]
        con.commit()
        self.sync_details(con)
        return self.__dict__

    async def update(self, con: connection) -> FoodOutletDetails:
        cursor = con.cursor()

        cursor.execute(
            f"UPDATE food_outlets SET name=%s, location=%s, landmark=%s, open_time=%s, close_time=%s, rating=%s, menu=%s, image=%s WHERE id={self.id}",
            (
                self.name,
                {
                    "latitude": self.location.latitude,
                    "longitude": self.location.longitude,
                },
                self.landmark,
                self.open_time,
                self.close_time,
                {"total": self.rating.total, "count": self.rating.count},
                self.menu,
                self.image,
            ),
        )
        con.commit()
        return self.__dict__

    async def remove(self, con: connection):
        cursor = con.cursor()

        cursor.execute(f"DELETE FROM food_outlets WHERE id={self.id}")
        con.commit()


async def searchOutlets(
    con: connection,
    nameFilter: Optional[str] = None,
    locationFilter: Optional[Location] = None,
    landmarkFilter: Optional[str] = None,
    timeFilter: Optional[time] = None,
    ratingFilter: Optional[int] = None,
) -> List[FoodOutletDetails]:
    cursor = con.cursor()

    cursor.execute(f"SELECT id FROM food_outlets")
    result = cursor.fetchall()

    outlets: List[FoodOutlet] = []

    for row in result:
        outlet = FoodOutlet(id=row[0])
        outlets.append(outlet)

    cursor.close()

    for outlet in outlets:
        await outlet.sync_details(con=con)

    if nameFilter is not None:
        for i in range(len(outlets)):
            try:
                if outlets[i].name.find(nameFilter) == -1:
                    outlets.pop(i)
                    i -= 1
            except IndexError:
                break

    if locationFilter is not None:
        latitude = float(locationFilter["latitude"])
        longitude = float(locationFilter["longitude"])
        user_location = (latitude, longitude)

        for j in range(len(outlets)):
            try:
                if outlets[j].location is not None:
                    outlet_location = (
                        float(outlets[j].location.latitude),
                        float(outlets[j].location.longitude),
                    )
                    distance = geopy.distance.geodesic(
                        user_location, outlet_location
                    ).km
                    if distance > 1:
                        outlets.pop(j)
                        j -= 1
                else:
                    outlets.pop(j)
                    j -= 1
            except IndexError:
                break

    if landmarkFilter is not None:
        for k in range(len(outlets)):
            try:
                if outlets[k].landmark is not None:
                    if outlets[k].landmark.find(landmarkFilter) == -1:
                        outlets.pop(k)
                        k -= 1
                else:
                    outlets.pop(k)
                    k -= 1
            except IndexError:
                break

    if timeFilter is not None:
        for l in range(len(outlets)):
            try:
                if (
                    outlets[l].open_time is not None
                    and outlets[l].close_time is not None
                ):
                    if (
                        outlets[l].open_time > timeFilter
                        or outlets[l].close_time < timeFilter
                    ):
                        outlets.pop(l)
                        l -= 1
                else:
                    outlets.pop(l)
                    l -= 1
            except IndexError:
                break

    if ratingFilter is not None:
        for m in range(len(outlets)):
            try:
                if outlets[m].rating is not None:
                    if outlets[m].rating.value < ratingFilter:
                        outlets.pop(m)
                        m -= 1
                else:
                    outlets.pop(m)
                    m -= 1
            except IndexError:
                break

    return outlets
