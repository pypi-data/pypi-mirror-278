from obfsc8.src.obfsc8.get_columns_to_be_obfuscated \
    import get_columns_to_be_obfuscated
from test_data.test_json import test_json
from test_data.test_json_targeting_student_id \
    import test_json_targeting_student_id


def test_that_list_returned():
    restricted_fields = []
    result = get_columns_to_be_obfuscated(test_json, restricted_fields)

    assert isinstance(result, list)


def test_that_list_contains_correct_column_names():
    restricted_fields = []
    result = get_columns_to_be_obfuscated(test_json, restricted_fields)

    assert result == ["name", "email_address"]


def test_that_restricted_fields_correctly_removed_from_column_names():
    restricted_fields = ["student_id"]
    result1 = (get_columns_to_be_obfuscated
               (test_json_targeting_student_id, restricted_fields))

    assert result1 == ["name", "email_address"]

    restricted_fields = []
    result2 = (get_columns_to_be_obfuscated
               (test_json_targeting_student_id, restricted_fields))

    assert result2 == ["student_id", "name", "email_address"]
