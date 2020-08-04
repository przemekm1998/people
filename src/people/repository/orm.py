from sqlalchemy import (
    Table, MetaData, Column, Integer, String, Date,
    ForeignKey
)
from sqlalchemy.orm import mapper, relationship

from src.people.domain_models.models import Name

metadata = MetaData()

names = Table(
    'names', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('title', String(2)),
    Column('first_name', String(50)),
    Column('second_name', String(50))
)


def start_mappers():
    names_mapper = mapper(Name, names)
