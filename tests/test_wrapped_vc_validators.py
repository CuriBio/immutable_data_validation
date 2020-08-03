# -*- coding: utf-8 -*-
import datetime
import uuid

from immutable_data_validation import validate_datetime
from immutable_data_validation import validate_float
from immutable_data_validation import validate_int
from immutable_data_validation import validate_str
from immutable_data_validation import validate_uuid
from immutable_data_validation.errors import ValidationCollectionCannotCoerceError
from immutable_data_validation.errors import ValidationCollectionEmptyValueError
from immutable_data_validation.errors import ValidationCollectionMaximumLengthError
from immutable_data_validation.errors import ValidationCollectionMaximumValueError
from immutable_data_validation.errors import ValidationCollectionMinimumLengthError
from immutable_data_validation.errors import ValidationCollectionMinimumValueError
from immutable_data_validation.errors import ValidationCollectionNotAnIntegerError
import pytest

GENERIC_UUID = uuid.uuid4()
GENERIC_DATETIME = datetime.datetime.now()

EMPTY_VALUE_ERROR_EXPECTED_TEXT = "was empty"


@pytest.mark.parametrize(
    "func,value,kwargs,expected_error,expected_text_in_error,test_description",
    [
        (
            validate_str,
            None,
            {"extra_error_msg": "errmsg26"},
            ValidationCollectionEmptyValueError,
            (EMPTY_VALUE_ERROR_EXPECTED_TEXT, "errmsg26"),
            "null value",
        ),
        (
            validate_str,
            None,
            {"allow_null": True},
            None,
            None,
            "allows None when specified",
        ),
        (
            validate_str,
            293,
            {"extra_error_msg": "errmsg25"},
            ValidationCollectionCannotCoerceError,
            ("was not coerced", "errmsg25"),
            "not a string",
        ),
        (
            validate_str,
            "a",
            {"minimum_length": 2, "extra_error_msg": "errmsg24"},
            ValidationCollectionMinimumLengthError,
            ("below the minimum length", "errmsg24"),
            "too short",
        ),
        (
            validate_str,
            "eli",
            {"maximum_length": 1, "extra_error_msg": "errmsg23"},
            ValidationCollectionMaximumLengthError,
            ("exceeds maximum length", "errmsg23"),
            "too long",
        ),
        (
            validate_uuid,
            None,
            {"extra_error_msg": "error message 7"},
            ValidationCollectionEmptyValueError,
            (EMPTY_VALUE_ERROR_EXPECTED_TEXT, "error message 7"),
            "null value",
        ),
        (
            validate_uuid,
            "notrealuuid",
            {"extra_error_msg": "what error"},
            ValidationCollectionCannotCoerceError,
            ("coerced to a valid UUID", "what error"),
            "not a uuid",
        ),
        (
            validate_uuid,
            None,
            {"allow_null": True},
            None,
            None,
            "allows None when specified",
        ),
        (
            validate_int,
            None,
            {"extra_error_msg": "bobs error"},
            ValidationCollectionEmptyValueError,
            (EMPTY_VALUE_ERROR_EXPECTED_TEXT, "bobs error"),
            "null value",
        ),
        (
            validate_int,
            None,
            {"allow_null": True},
            None,
            None,
            "allows None when specified",
        ),
        (
            validate_int,
            293.9,
            {"extra_error_msg": "error things"},
            ValidationCollectionNotAnIntegerError,
            ("not an integer-type", "error things"),
            "not an int",
        ),
        (
            validate_int,
            -1,
            {"minimum": 0, "extra_error_msg": "error stuff"},
            ValidationCollectionMinimumValueError,
            ("less than minimum", "error stuff"),
            "too low",
        ),
        (
            validate_int,
            300,
            {"maximum": 200, "extra_error_msg": "error info"},
            ValidationCollectionMaximumValueError,
            ("exceeds maximum (", "error info"),
            "too high",
        ),
        (
            validate_int,
            "bob",
            {"extra_error_msg": "error9928"},
            ValidationCollectionCannotCoerceError,
            ("coerced to a numeric", "error9928"),
            "a string",
        ),
        (
            validate_datetime,
            None,
            {"extra_error_msg": "special error info"},
            ValidationCollectionEmptyValueError,
            (EMPTY_VALUE_ERROR_EXPECTED_TEXT, "special error info"),
            "null value",
        ),
        (
            validate_datetime,
            None,
            {"allow_null": True},
            None,
            None,
            "allows None when specified",
        ),
        (
            validate_datetime,
            "two thousand nineteen",
            {"extra_error_msg": "new message"},
            ValidationCollectionCannotCoerceError,
            ("datetime object", "new message"),
            "not a datetime",
        ),
        (
            validate_datetime,
            GENERIC_DATETIME,
            {
                "minimum": datetime.date(year=5000, month=2, day=5),
                "extra_error_msg": "mymessage",
            },
            ValidationCollectionMinimumValueError,
            ("is before the minimum", "mymessage"),
            "too soon",
        ),
        (
            validate_datetime,
            GENERIC_DATETIME,
            {
                "maximum": datetime.date(year=1990, month=2, day=5),
                "extra_error_msg": "dates and times",
            },
            ValidationCollectionMaximumValueError,
            ("after the maximum", "dates and times"),
            "too late",
        ),
        (
            validate_float,
            None,
            {"extra_error_msg": "what a float"},
            ValidationCollectionEmptyValueError,
            [EMPTY_VALUE_ERROR_EXPECTED_TEXT, "what a float"],
            "null value",
        ),
        (
            validate_float,
            None,
            {"allow_null": True},
            None,
            None,
            "allows None when specified",
        ),
        (
            validate_float,
            "pi",
            {"extra_error_msg": "cool float"},
            ValidationCollectionCannotCoerceError,
            ["coerced to a numeric form", "cool float"],
            "not a float",
        ),
        (
            validate_float,
            -1,
            {"minimum": 0},
            ValidationCollectionMinimumValueError,
            "less than minimum",
            "too low",
        ),
        (
            validate_float,
            300,
            {"maximum": 200},
            ValidationCollectionMaximumValueError,
            "exceeds maximum (",
            "too high",
        ),
        (
            validate_float,
            300,
            {
                "maximum": 200,
                "minimum": 23,
                "extra_error_msg": "my_favorite_float is cool",
            },
            ValidationCollectionMaximumValueError,
            " my_favorite_float is cool",
            "extra info in error message",
        ),
        (
            validate_float,
            5,
            {
                "maximum": 200,
                "minimum": 23,
                "extra_error_msg": "my_favorite_float is cool",
            },
            ValidationCollectionMinimumValueError,
            " my_favorite_float is cool",
            "extra info in error message",
        ),
    ],
)
def test_wrapped_error(
    func, value, kwargs, expected_error, expected_text_in_error, test_description
):
    if kwargs is None:
        kwargs = dict()

    def run_func():
        return func(value, **kwargs)

    if expected_error is not None:
        with pytest.raises(expected_error) as e:
            run_func()
        if expected_text_in_error is not None:
            if not isinstance(expected_text_in_error, (list, tuple)):
                expected_text_in_error = [expected_text_in_error]
            for this_expected_text_in_error in expected_text_in_error:
                assert this_expected_text_in_error in str(e)
    else:
        run_func()


@pytest.mark.parametrize(
    "func,value,kwargs,expected,test_description",
    [
        (validate_str, "bob", None, "bob", "standard"),
        (validate_uuid, GENERIC_UUID, None, GENERIC_UUID, "standard"),
        (validate_int, 173, None, 173, "standard"),
        (validate_datetime, GENERIC_DATETIME, None, GENERIC_DATETIME, "standard"),
        (validate_float, 3.1415, None, 3.1415, "standard"),
    ],
)
def test_returns_valid_value(func, value, kwargs, expected, test_description):
    if kwargs is None:
        kwargs = dict()

    actual = func(value, **kwargs)
    assert actual == expected
