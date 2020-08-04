# -*- coding: utf-8 -*-
import datetime

from immutable_data_validation import validate_crc32
from immutable_data_validation import validate_sql_utc_datetime
from immutable_data_validation import validate_utc_datetime
from immutable_data_validation.errors import MicrosecondsInSqlTimeError
from immutable_data_validation.errors import MissingTimezoneError
from immutable_data_validation.errors import TimezoneNotUtcError
from immutable_data_validation.errors import ValidationCollectionCannotCoerceError
from immutable_data_validation.errors import ValidationCollectionEmptyValueError
from immutable_data_validation.errors import ValidationCollectionMaximumLengthError
from immutable_data_validation.errors import ValidationCollectionMaximumValueError
from immutable_data_validation.errors import ValidationCollectionMinimumLengthError
from immutable_data_validation.errors import ValidationCollectionMinimumValueError
import pytest
import pytz

GENERIC_UTC_DATETIME = datetime.datetime(
    year=2019,
    month=5,
    day=29,
    hour=15,
    minute=36,
    second=22,
    microsecond=2932,
    tzinfo=datetime.timezone.utc,
)


def test_validate_utc_datetime__raises_error_if_not_datetime():
    with pytest.raises(ValidationCollectionCannotCoerceError):
        validate_utc_datetime("billy")


def test_validate_utc_datetime__passes_extra_error_msg_down_to_wrapped_validators():
    with pytest.raises(ValidationCollectionEmptyValueError) as e:
        validate_utc_datetime(None, extra_error_msg="errmsg30")
    assert "errmsg30" in str(e)


def test_validate_utc_datetime__raises_error_if_timezone_naive():
    with pytest.raises(MissingTimezoneError) as e:
        validate_utc_datetime(datetime.datetime.utcnow(), extra_error_msg="errmsg31")
    assert "errmsg31" in str(e)


def test_validate_utc_datetime__passes_if_utc():
    expected_datetime = datetime.datetime.now(datetime.timezone.utc)
    actual_datetime = validate_utc_datetime(expected_datetime)
    assert actual_datetime == expected_datetime


def test_validate_utc_datetime__raises_error_if_timezone_not_utc():
    test_time = datetime.datetime.now(pytz.timezone("US/Eastern"))
    with pytest.raises(TimezoneNotUtcError) as e:
        validate_utc_datetime(test_time, extra_error_msg="errmsg32")
    assert "errmsg32" in str(e)


def test_validate_utc_datetime__raises_error_if_before_minimum():
    with pytest.raises(ValidationCollectionMinimumValueError) as e:
        validate_utc_datetime(
            GENERIC_UTC_DATETIME,
            minimum=GENERIC_UTC_DATETIME + datetime.timedelta(seconds=1),
            extra_error_msg="errmsg390",
        )
    assert "errmsg390" in str(e)


def test_validate_utc_datetime__raises_error_if_after_maximum():
    with pytest.raises(ValidationCollectionMaximumValueError) as e:
        validate_utc_datetime(
            GENERIC_UTC_DATETIME,
            maximum=GENERIC_UTC_DATETIME - datetime.timedelta(seconds=1),
            extra_error_msg="errmsg391",
        )
    assert "errmsg391" in str(e)


def test_validate_sql_utc_datetime__strips_microseconds_when_coerce_set_to_true():
    test_time = datetime.datetime(
        year=2019,
        month=5,
        day=29,
        hour=15,
        minute=36,
        second=22,
        microsecond=2932,
        tzinfo=datetime.timezone.utc,
    )
    actual_datetime = validate_sql_utc_datetime(test_time)
    assert actual_datetime.microsecond == 0


def test_validate_sql_utc_datetime__raises_error_if_microseconds_present_and_coerce_set_to_false():
    test_time = datetime.datetime(
        year=2019,
        month=5,
        day=29,
        hour=15,
        minute=36,
        second=22,
        microsecond=2932,
        tzinfo=datetime.timezone.utc,
    )
    with pytest.raises(MicrosecondsInSqlTimeError) as e:
        validate_sql_utc_datetime(
            test_time, coerce_value=False, extra_error_msg="errmsg28"
        )
    assert "errmsg28" in str(e)


def test_validate_sql_utc_datetime__passes_extra_error_msg_down_to_wrapped_validators():
    with pytest.raises(ValidationCollectionEmptyValueError) as e:
        validate_sql_utc_datetime(None, extra_error_msg="errmsg29")
    assert "errmsg29" in str(e)


def test_validate_sql_utc_datetime__raises_error_if_before_minimum():
    with pytest.raises(ValidationCollectionMinimumValueError) as e:
        validate_sql_utc_datetime(
            GENERIC_UTC_DATETIME,
            minimum=GENERIC_UTC_DATETIME + datetime.timedelta(seconds=1),
            extra_error_msg="errmsg393",
        )
    assert "errmsg393" in str(e)


def test_validate_sql_utc_datetime__raises_error_if_after_maximum():
    with pytest.raises(ValidationCollectionMaximumValueError) as e:
        validate_sql_utc_datetime(
            GENERIC_UTC_DATETIME,
            maximum=GENERIC_UTC_DATETIME - datetime.timedelta(seconds=1),
            extra_error_msg="errmsg394",
        )
    assert "errmsg394" in str(e)


@pytest.mark.parametrize(
    "the_func,value,kwargs,expected_error,expected_text_in_the_error,test_description",
    [
        (
            validate_utc_datetime,
            None,
            {"allow_null": True},
            None,
            None,
            "allow None when specified",
        ),
        (
            validate_sql_utc_datetime,
            None,
            {"allow_null": True},
            None,
            None,
            "allow None when specified",
        ),
        (
            validate_crc32,
            393,
            {"extra_error_msg": "errmsg27"},
            ValidationCollectionCannotCoerceError,
            ("not coerced to a str", "errmsg27"),
            "not a string",
        ),
        (
            validate_crc32,
            None,
            {"allow_null": True},
            None,
            None,
            "allow None when specified",
        ),
        (
            validate_crc32,
            "393abc",
            None,
            ValidationCollectionMinimumLengthError,
            "below the minimum",
            "too short",
        ),
        (
            validate_crc32,
            "3939abcdf",
            None,
            ValidationCollectionMaximumLengthError,
            "exceeds maximum",
            "too long",
        ),
    ],
)
def test_error(
    the_func,
    value,
    kwargs,
    expected_error,
    expected_text_in_the_error,
    test_description,
):
    if kwargs is None:
        kwargs = dict()

    def run_the_func():
        return the_func(value, **kwargs)

    if expected_error is not None:
        with pytest.raises(expected_error) as e:
            run_the_func()
        if expected_text_in_the_error is not None:
            if not isinstance(expected_text_in_the_error, (list, tuple)):
                expected_text_in_the_error = [expected_text_in_the_error]
            for this_expected_text_in_error in expected_text_in_the_error:
                assert this_expected_text_in_error in str(e)
    else:
        run_the_func()


@pytest.mark.parametrize(
    "func,value,kwargs,expected,test_description",
    [(validate_crc32, "a910bco3", None, "a910bco3", "standard")],
)
def test_func_returns_valid_value(func, value, kwargs, expected, test_description):
    if kwargs is None:
        kwargs = dict()

    actual_value = func(value, **kwargs)
    assert actual_value == expected
