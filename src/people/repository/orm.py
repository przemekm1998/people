from sqlalchemy import (
    Table, MetaData, Column, Integer, String, Date,
    ForeignKey, Float
)
from sqlalchemy.orm import mapper, relationship

from src.people.domain_models.models import Name, Timezone, Coordinates, Location

metadata = MetaData()

names = Table(
    'names', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('title', String(2)),
    Column('first_name', String(50)),
    Column('second_name', String(50))
)

timezones = Table(
    'timezones', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('offset', String(10)),
    Column('description', String(30))
)

coordinates = Table(
    'coordinates', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('latitude', Float),
    Column('longitude', Float)
)

locations = Table(
    'locations', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('street', String(50)),
    Column('city', String(50)),
    Column('state', String(50)),
    Column('postcode', String(5)),
    Column('timezone', ForeignKey('timezones.id')),
    Column('coordinates', ForeignKey('coordinates.id'))
)


def start_mappers():
    names_mapper = mapper(Name, names)
    timezones_mapper = mapper(Timezone, timezones)
    coordinates_mapper = mapper(Coordinates, coordinates)
    locations_mapper = mapper(Location, locations)
