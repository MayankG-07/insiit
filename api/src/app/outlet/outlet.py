from typing import Optional
from appTypes.globalTypes import Location, Rating
from appTypes.outletTypes import FoodOutletMenu, FoodOutletDetails
from datetime import time
from fastapi import HTTPException, status


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

    def sync_details(self, con):
        cursor = con.cursor()

        if self.id is not None:
            cursor.execute(f"SELECT * FROM food_outlets WHERE id={self.id}")
        elif self.name is not None:
            cursor.execute(f"SELECT * FROM food_outlets WHERE name='{self.name}'")
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Insufficient data"
            )

        result = cursor.fetchone()

        try:
            self.id = result[0]
            self.name = result[1]
            self.location = result[2]
            self.landmark = result[3]
            self.open_time = result[4]
            self.close_time = result[5]
            self.rating = result[6]
            self.menu = result[7]
            self.image = result[8]
        except TypeError:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Food outlet not found"
            )

    def create(self, con):
        cursor = con.cursor()

        cursor.execute(
            "INSERT INTO food_outlets(name, location, landmark, open_time, close_time, rating, menu, image) VALUES(%s, %s, %s, %s, %s, %s, %s, %s) RETURNING id",
            (
                self.name,
                self.location,
                self.landmark,
                self.open_time,
                self.close_time,
                self.rating,
                self.menu,
                self.image,
            ),
        )

        self.id = cursor.fetchone()[0]
        con.commit()
        self.sync_details(con)
        return self.__dict__

    def remove(self, con):
        cursor = con.cursor()

        cursor.execute(f"DELETE FROM food_outlets WHERE id={self.id}")
        con.commit()
