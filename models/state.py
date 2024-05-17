#!/usr/bin/python3
""" State Module for HBNB project """
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from models import storage_type
from models.base_model import Base, BaseModel


class State(BaseModel, Base):
    """ State class """

    if storage_type == "db":
        __tablename__ = "states"

        name = Column(String(128), nullable=False)
        cities = relationship("City", backref="state")
    else:
        name = ""

    def __init__(self, *args, **kwargs):
        """initializes State"""
        super().__init__(*args, **kwargs)

    if storage_type != "db":

        @property
        def cities(self):
            """returns the list of City instances"""
            from models import storage
            from models.city import City

            cities_instances = []
            all_cities = storage.all(City)

            for city in all_cities.values():
                if city.state_id == self.id:
                    cities_instances.append(city)

            return cities_instances
