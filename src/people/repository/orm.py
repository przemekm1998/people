from sqlalchemy import (
    Table, MetaData, Column, Integer, String, Date,
    ForeignKey, Float
)
from sqlalchemy.orm import mapper, relationship

from src.people.domain_models.models import Timezone, Coordinates, Location, User, \
    Person, ContactInfo, PersonalId, Nat

metadata = MetaData()

user = Table(
    'user', metadata,
    Column('uuid', String, primary_key=True),
    Column('username', String(50)),
    Column('password', String),
    Column('salt', String),
    Column('md5', String),
    Column('sha1', String),
    Column('sha256', String),
    Column('date_registered', Date),
)

person = Table(
    'person', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('gender', String(20)),
    Column('title', String(2)),
    Column('first_name', String(50)),
    Column('second_name', String(50)),
    Column('date_of_birth', Date),
    Column('user_uuid', Integer, ForeignKey('user.uuid'))
)

contact_info = Table(
    'contact_info', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('phone', String),
    Column('cell', String),
    Column('email', String),
    Column('user_uuid', Integer, ForeignKey('user.uuid'))
)

timezone = Table(
    'timezone', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('offset', String(10)),
    Column('description', String(30), unique=True),
)

coordinates = Table(
    'coordinates', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('latitude', Float),
    Column('longitude', Float),
)

nat = Table(
    'nat', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('name', String(2), unique=True)
)

location = Table(
    'location', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('street', String(50)),
    Column('city', String(50)),
    Column('state', String(50)),
    Column('postcode', String(5)),
    Column('timezone_id', Integer, ForeignKey('timezone.id')),
    Column('coordinates_id', Integer, ForeignKey('coordinates.id')),
    Column('nat_id', Integer, ForeignKey('nat.id')),
    Column('user_id', Integer, ForeignKey('user.uuid'))
)

personal_id = Table(
    'personal_id', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('name', String),
    Column('value', String),
    Column('user_id', Integer, ForeignKey('user.uuid'))
)


def start_mappers():
    location_mapper = mapper(Location, location)
    mapper(Timezone, timezone, properties={
        'locations': relationship(location_mapper, backref='timezone')
    })
    mapper(Coordinates, coordinates, properties={
        'locations': relationship(location_mapper, backref='coordinates')
    })
    mapper(Nat, nat, properties={
        'locations': relationship(location_mapper, backref='nat')
    })

    person_mapper = mapper(Person, person)
    contact_info_mapper = mapper(ContactInfo, contact_info)
    personal_id_mapper = mapper(PersonalId, personal_id)
    mapper(User, user, properties={
        'person': relationship(person_mapper, backref='user', uselist=False),
        'contact_info': relationship(contact_info_mapper, backref='user',
                                     uselist=False),
        'location': relationship(location_mapper, backref='user', uselist=False),
        'personal_id': relationship(personal_id_mapper, backref='user', uselist=False)
    })
