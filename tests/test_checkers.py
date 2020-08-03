# -*- coding: utf-8 -*-
import datetime

from immutable_data_validation import is_utc_datetime
from immutable_data_validation import is_uuid
import pytz


def test_is_utc_datetime__returns_true_if_utc():
    test_time = datetime.datetime.now(datetime.timezone.utc)
    assert is_utc_datetime(test_time) is True


def test_is_utc_datetime__returns_true_if_pytz_utc():
    test_time = datetime.datetime.now(pytz.utc)
    assert is_utc_datetime(test_time) is True


def test_is_utc_datetime__returns_false_if_timezone_naive():
    test_time = datetime.datetime.utcnow()
    assert is_utc_datetime(test_time) is False


def test_is_utc_datetime__returns_false_if_timezone_not_utc():
    test_time = datetime.datetime.now(pytz.timezone("US/Eastern"))
    assert is_utc_datetime(test_time) is False


def test_is_utc_datetime__returns_false_for_int():
    assert is_utc_datetime(5) is False


def test_is_uuid__returns_true_for_valid_uuid():
    assert is_uuid("2dc06596-9cea-46a2-9ddd-a0d8a0f13584") is True


def test_is_uuid__returns_false__when_uuid_is_empty():
    assert is_uuid("") is False


def test_is_uuid__returns_false__when_uuid_is_invalid():
    assert is_uuid("e140e2b-397a-427b-81f3-4f889c5181a9") is False
