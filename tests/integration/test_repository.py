# from datetime import date
#
# import pytest
#
# from src.people.domain_models.models import User, Person
# from src.people.repository.exceptions import RepositoryException
# from src.people.repository.repository import SqlAlchemyRepository
#
#
# def insert_user(session, uuid, username, password, salt, md5, sha1, sha256,
#                 date_registered):
#     session.execute(
#         'INSERT INTO "user" (uuid, username, password, salt, md5, sha1, sha256, '
#         'date_registered) VALUES '
#         '(:uuid, :username, :password, :salt, :md5, :sha1, :sha256, :date_registered)',
#         dict(uuid=uuid, username=username, password=password, salt=salt, md5=md5,
#              sha1=sha1, sha256=sha256, date_registered=date_registered)
#     )
#     [[user_id]] = session.execute(
#         'SELECT id FROM user WHERE uuid=:uuid',
#         dict(uuid=uuid)
#     )
#
#     return user_id
#
#
# def insert_person(session, gender, title, first_name, second_name, date_of_birth,
#                   user_id):
#     session.execute(
#         'INSERT INTO "person" (gender, title, first_name, second_name, date_of_birth, user_id) '
#         'VALUES '
#         '(:gender, :title, :first_name, :second_name, :date_of_birth, :user_id)',
#         dict(gender=gender, title=title, first_name=first_name,
#              second_name=second_name, date_of_birth=date_of_birth, user_id=user_id)
#     )
#     [[person_id]] = session.execute(
#         'SELECT id FROM person WHERE user_id=:user_id',
#         dict(user_id=user_id)
#     )
#
#     return person_id
#
#
# def populated_db_fixture(session):
#     user_id_1 = insert_user(session, 'uuid', 'username', 'password', 'salt', 'md5',
#                             'sha1', 'sha256', '1997-01-01')
#     insert_person(session, 'male', 'mr', 'john', 'doe', '1997-01-01',
#                   user_id_1)
#     user_id_2 = insert_user(session, 'uuid2', 'username', 'password', 'salt', 'md5',
#                             'sha1', 'sha256', '1997-01-01')
#     insert_person(session, 'male', 'mr', 'john', 'doe', '1998-01-01',
#                   user_id_2)
#     user_id_3 = insert_user(session, 'uuid3', 'username', 'password', 'salt', 'md5',
#                             'sha1', 'sha256', '1997-01-01')
#     insert_person(session, 'female', 'mr', 'john', 'doe', '1999-01-01',
#                   user_id_3)
#
#
# def test_repository_can_save_user(session):
#     user = User('uuid', 'user', 'password', 'salt', 'md5', 'sha1', 'sha256',
#                 date.fromisoformat('1997-01-01'))
#
#     repo = SqlAlchemyRepository(session)
#     repo.add(user)
#     session.commit()
#
#     rows = list(session.execute(
#         'SELECT * FROM user'
#     ))
#     assert rows == [
#         (1, 'uuid', 'user', 'password', 'salt', 'md5', 'sha1', 'sha256',
#          '1997-01-01')]
#
#
# def test_repository_can_retrieve_user(session):
#     user_id = insert_user(session, 'uuid', 'username', 'password', 'salt', 'md5',
#                           'sha1', 'sha256', '1997-01-01')
#     insert_person(session, 'male', 'mr', 'john', 'doe', '1997-01-01',
#                   user_id)
#
#     repo = SqlAlchemyRepository(session)
#     retrieved = repo.get(User, user_id)
#
#     expected_user = User('uuid', 'username', 'password', 'salt', 'md5',
#                          'sha1', 'sha256', date.fromisoformat('1997-01-01'))
#
#     assert retrieved.uuid == expected_user.uuid
#     assert retrieved.username == expected_user.username
#     assert retrieved.salt == expected_user.salt
#     assert retrieved.md5 == expected_user.md5
#     assert retrieved.sha1 == expected_user.sha1
#     assert retrieved.sha256 == expected_user.sha256
#     assert retrieved.date_registered == expected_user.date_registered
#     assert retrieved.password_strength == expected_user.password_strength
#
#
# def test_repository_can_retrieve_user_with_person(session):
#     user_id = insert_user(session, 'uuid', 'username', 'password', 'salt', 'md5',
#                           'sha1', 'sha256', '1997-01-01')
#     person_id = insert_person(session, 'male', 'mr', 'john', 'doe', '1997-01-01',
#                               user_id)
#
#     repo = SqlAlchemyRepository(session)
#     retrieved = repo.get(Person, person_id)
#
#     expected_user = User('uuid', 'username', 'password', 'salt', 'md5',
#                          'sha1', 'sha256', date.fromisoformat('1997-01-01'))
#     expected_person = Person('male', 'mr', 'john', 'doe', date.fromisoformat(
#         '1997-01-01'), expected_user)
#
#     assert retrieved.gender == expected_person.gender
#     assert retrieved.title == expected_person.title
#     assert retrieved.first_name == expected_person.first_name
#     assert retrieved.second_name == expected_person.second_name
#     assert retrieved.date_of_birth == expected_person.date_of_birth
#     assert retrieved.age == expected_person.age
#     assert retrieved.days_to_birthday == expected_person.days_to_birthday
#
#
# def test_repository_group_by(session):
#     populated_db_fixture(session)
#
#     repo = SqlAlchemyRepository(session)
#     retrieved = repo.group_by_and_count(Person, 'gender', limit=1)
#
#     assert retrieved[0][0].gender == 'male'
#     assert retrieved[0][1] == 2
#
#
# def test_repository_group_by_not_existing_column(session):
#     populated_db_fixture(session)
#
#     repo = SqlAlchemyRepository(session)
#     with pytest.raises(RepositoryException):
#         retrieved = repo.group_by_and_count(Person, 'idontexist', limit=1)
#
#
# def test_repository_filter_by_between(session):
#     populated_db_fixture(session)
#
#     repo = SqlAlchemyRepository(session)
#     retrieved = repo.filter_person_by_date_of_birth(date.fromisoformat('1998-01-01'),
#                                                     date.fromisoformat('1999-01-01'))
#
#     assert len(retrieved) == 2
#     assert retrieved[0].date_of_birth == date.fromisoformat('1998-01-01')
#     assert retrieved[1].date_of_birth == date.fromisoformat('1999-01-01')
#
#
# def test_filter_by(session):
#     populated_db_fixture(session)
#
#     repo = SqlAlchemyRepository(session)
#     filters = {'gender': 'male', 'date_of_birth': date.fromisoformat('1998-01-01')}
#     retrieved = repo.filter_model_by(Person, **filters)
#
#     assert retrieved[0].gender == 'male'
#     assert retrieved[0].date_of_birth == date.fromisoformat('1998-01-01')
#
#
# def test_filter_by_not_existing_columns(session):
#     populated_db_fixture(session)
#
#     repo = SqlAlchemyRepository(session)
#     filters = {'idontexist': 'male', 'andmetoo': date.fromisoformat('1998-01-01')}
#
#     with pytest.raises(RepositoryException):
#         retrieved = repo.filter_model_by(Person, **filters)
#
