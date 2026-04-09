import pytest

from app.switchboard import Switchboard
from app.users import ForeignUser, LocalUser


# Happy Route(no errors)
def test_register_call_creates_local_and_foreign_users() -> None:
    switchboard = Switchboard()

    active_call = switchboard.register_call(
        "1,Ivan Ivanov,+79990000000,2,John Smith,+15551234567"
    )

    assert isinstance(active_call.caller, LocalUser)
    assert isinstance(active_call.receiver, ForeignUser)
    assert active_call.caller.id == 1
    assert active_call.receiver.id == 2


def test_register_call_counts_active_calls() -> None:
    switchboard = Switchboard()

    switchboard.register_call(
        "1,Ivan Ivanov,+79990000000,2,Petr Petrov,+78880000000"
    )
    switchboard.register_call(
        "3,John Smith,+15551234567,4,Jane Doe,+33123456789"
    )

    assert switchboard.get_active_calls_count() == 2


def test_register_call_counts_calls_between_local_and_foreign_users() -> None:
    switchboard = Switchboard()

    switchboard.register_call(
        "1,Ivan Ivanov,+79990000000,2,John Smith,+15551234567"
    )
    switchboard.register_call(
        "3,Petr Petrov,+78880000000,4,Maria Petrova,+79991112233"
    )
    switchboard.register_call(
        "5,Jane Doe,+33123456789,6,Alex Doe,+442012345678"
    )

    assert switchboard.get_active_calls_count() == 3
    assert switchboard.get_cross_border_calls_count() == 1


def test_register_call_creates_two_local_users() -> None:
    switchboard = Switchboard()

    active_call = switchboard.register_call(
        "1,Ivan Ivanov,+79990000000,2,Petr Petrov,+78880000000"
    )

    assert isinstance(active_call.caller, LocalUser)
    assert isinstance(active_call.receiver, LocalUser)
    assert not active_call.is_cross_border


def test_register_call_creates_two_foreign_users() -> None:
    switchboard = Switchboard()

    active_call = switchboard.register_call(
        "1,John Smith,+15551234567,2,Jane Doe,+33123456789"
    )

    assert isinstance(active_call.caller, ForeignUser)
    assert isinstance(active_call.receiver, ForeignUser)
    assert not active_call.is_cross_border


def test_calls_count_starts_at_zero() -> None:
    switchboard = Switchboard()

    assert switchboard.get_active_calls_count() == 0
    assert switchboard.get_cross_border_calls_count() == 0


def test_cross_border_calls_from_both_sides_count() -> None:
    switchboard = Switchboard()

    switchboard.register_call(
        "1,Ivan Ivanov,+79990000000,2,John Smith,+15551234567"
    )
    switchboard.register_call(
        "3,Petr Petrov,+78880000000,4,Maria Petrova,+79991112233"
    )
    switchboard.register_call(
        "5,John Dough,+15551234567,6,Ivan Smirnov,+79990000000"
    )

    assert switchboard.get_cross_border_calls_count() == 2


def test_active_calls_count() -> None:
    switchboard = Switchboard()

    switchboard.register_call(
        "1,Ivan Ivanov,+79990000000,2,John Smith,+15551234567"
    )
    switchboard.register_call(
        "3,Petr Petrov,+78880000000,4,Maria Petrova,+79991112233"
    )
    switchboard.register_call(
        "5,Jane Doe,+33123456789,6,Alex Doe,+442012345678"
    )

    assert switchboard.get_active_calls_count() == 3


# Sad route( Errors :`( )
def test_register_raises_on_too_few_fields() -> None:
    switchboard = Switchboard()

    with pytest.raises(ValueError):
        switchboard.register_call("1,Ivan Ivanov,+79990000000")


def test_register_raises_on_empty_string() -> None:
    switchboard = Switchboard()

    with pytest.raises(ValueError):
        switchboard.register_call("")


def test_register_raises_on_non_integer_id() -> None:
    switchboard = Switchboard()

    with pytest.raises(ValueError):
        switchboard.register_call("abc,Ivan Ivanov,+79990000000,2,Petr Petrov,+78880000000")


def test_register_raises_on_empty_fullname() -> None:
    switchboard = Switchboard()

    with pytest.raises(ValueError):
        switchboard.register_call("1,,+79990000000,2,Petr Petrov,+78880000000")


def test_register_raises_on_blank_fullname() -> None:
    switchboard = Switchboard()

    with pytest.raises(ValueError):
        switchboard.register_call("1,   ,+79990000000,2,Petr Petrov,+78880000000")


def test_register_raises_on_numeric_fullname() -> None:
    switchboard = Switchboard()

    with pytest.raises(ValueError):
        switchboard.register_call("1,12345,+79990000000,2,Petr Petrov,+78880000000")


def test_register_raises_on_invalid_phone() -> None:
    switchboard = Switchboard()

    with pytest.raises(ValueError):
        switchboard.register_call("1,Ivan Ivanov,79990000000,2,Petr Petrov,+78880000000")


def test_register_raises_on_phone_prefix_only() -> None:
    switchboard = Switchboard()

    with pytest.raises(ValueError):
        switchboard.register_call("1,Ivan Ivanov,+,2,Petr Petrov,+78880000000")