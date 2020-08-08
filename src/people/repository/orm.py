from sqlalchemy import (
    Table, MetaData, Column, Integer, String, Date,
    ForeignKey, Float, UniqueConstraint
)
from sqlalchemy.orm import mapper, relationship

from src.people.domain_models.models import Timezone, Coordinates, Location, \
    Person, ContactInfo, PersonalId, Nat, User, LoginInfo

metadata = MetaData()

user = Table(
    'user', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('person_id', Integer, ForeignKey('person.id'), nullable=False),
    Column('login_info_id', Integer, ForeignKey('login_info.id'), nullable=False),
    Column('contact_info_id', Integer, ForeignKey('contact_info.id'), nullable=False),
    Column('location_info_id', Integer, ForeignKey('location.id')),
    Column('personal_id_id', Integer, ForeignKey('personal_id.id'))
)

person = Table(
    'person', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('gender', String(20)),
    Column('title', String(2)),
    Column('first_name', String(50)),
    Column('second_name', String(50)),
    Column('date_of_birth', Date),
)

login_info = Table(
    'login_info', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('uuid', String, unique=True),
    Column('username', String(50), unique=True),
    Column('password', String),
    Column('salt', String),
    Column('md5', String),
    Column('sha1', String),
    Column('sha256', String),
    Column('date_registered', Date),
)

contact_info = Table(
    'contact_info', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('phone', String),
    Column('cell', String),
    Column('email', String),
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
    UniqueConstraint('latitude', 'longitude')
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
)

personal_id = Table(
    'personal_id', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('name', String),
    Column('value', String),
)


def start_mappers():
    user_mapper = mapper(User, user)
    person_mapper = mapper(Person, person, properties={
        'user': relationship(user_mapper, backref='person', uselist=False)
    })
    location_mapper = mapper(Location, location, properties={
        'person': relationship(user_mapper, backref='location', uselist=False)
    })
    mapper(Timezone, timezone, properties={
        'locations': relationship(location_mapper, backref='timezone')
    })
    mapper(Coordinates, coordinates, properties={
        'locations': relationship(location_mapper, backref='coordinates')
    })
    mapper(Nat, nat, properties={
        'locations': relationship(location_mapper, backref='nat')
    })
    login_info_mapper = mapper(LoginInfo, login_info, properties={
        'person': relationship(user_mapper, backref='login_info', uselist=False)
    })
    contact_info_mapper = mapper(ContactInfo, contact_info, properties={
        'person': relationship(user_mapper, backref='contact_info', uselist=False)
    })
    personal_id_mapper = mapper(PersonalId, personal_id, properties={
        'person': relationship(user_mapper, backref='personal_id', uselist=False)
    })
