from src.people.domain_models.models import Name


def test_name_mapper_can_load_names(session):
    session.execute(
        'INSERT INTO "names" (title, first_name, second_name) VALUES '
        '("Mr", "John", "Doe"),'
        '("Ms", "Jane", "Doe")'
    )
    expected = [
        Name("Mr", "John", "Doe"),
        Name("Ms", "Jane", "Doe")
    ]
    assert session.query(Name).all() == expected


def test_name_mapper_can_save_names(session):
    new_name = Name("Mr", "John", "Doe")
    session.add(new_name)
    session.commit()

    rows = list(session.execute('SELECT * FROM "names"'))
    assert rows == [(1, "Mr", "John", "Doe")]
