import pytest
import sqlalchemy

from src.people.domain_models.models import Timezone, Coordinates, Location, Nat, User


def test_user_mapper(session, user_factory_fixture):
    user = user_factory_fixture()

    session.add(user)
    db_user = session.query(User).one()

    assert user == db_user


def test_login_info_unique_constraint(session, login_info_factory_fixture):
    login_info_1 = login_info_factory_fixture()
    login_info_2 = login_info_factory_fixture()

    with pytest.raises(sqlalchemy.exc.IntegrityError):
        session.add(login_info_1)
        session.add(login_info_2)
        session.commit()


def test_coordinates_unique_constraint(session, coordinates_factory_fixture):
    coordinates_1 = coordinates_factory_fixture()
    coordinates_2 = coordinates_factory_fixture()

    with pytest.raises(sqlalchemy.exc.IntegrityError):
        session.add(coordinates_1)
        session.add(coordinates_2)
        session.commit()
