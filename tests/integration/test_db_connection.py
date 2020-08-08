# from datetime import date
#
# import pytest
#
# from src.people.domain_models.models import User
# from src.people.service_layer.db_connection import SqlAlchemyDbConnection
#
#
# def try_to_add_user(session):
#     user = User('uuid', 'username', 'password', 'salt', 'md5',
#                 'sha1', 'sha256', date.fromisoformat('1997-01-01'))
#
#     with SqlAlchemyDbConnection() as conn:
#         conn.database.add(user)
#
#     db_user = session.execute(
#         'SELECT * FROM user WHERE user_uuid=:user_uuid',
#         dict(user_uuid='uuid')
#     )
#
#     assert db_user == user
#
#
# def test_db_connection_rollback_on_error(session):
#     class MyException(Exception):
#         pass
#
#     user = User('uuid', 'username', 'password', 'salt', 'md5',
#                 'sha1', 'sha256', date.fromisoformat('1997-01-01'))
#
#     with pytest.raises(MyException):
#         with SqlAlchemyDbConnection() as conn:
#             conn.database.add(user)
#             raise MyException()
#
#     users = session.execute('SELECT * FROM "user"')
#     assert users.fetchall() == []
