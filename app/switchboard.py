from __future__ import annotations

from dataclasses import dataclass

from app.users import User, ForeignUser, LocalUser


LOCAL_PHONE_PREFIX = "+7"


def _validate_fullname(fullname: str) -> bool:
    return bool(fullname.strip()) and all(char.isalpha() or char.isspace() for char in fullname)


def _validate_id(raw_id: str) -> bool:
    return bool(raw_id) and all(char.isdigit() for char in raw_id)


def _validate_phone(raw_phone: str) -> bool:
    return raw_phone.startswith('+') and all(char.isdigit() for char in raw_phone[1:]) and len(raw_phone) > 1


def _validate_call_parts(parts: list[str]) -> None:
    caller_id, caller_fullname, caller_phone, receiver_id, receiver_fullname, receiver_phone = parts

    if not (_validate_fullname(caller_fullname) and _validate_fullname(receiver_fullname)):
        raise ValueError("Invalid fullname")

    if not (_validate_id(caller_id) and _validate_id(receiver_id)):
        raise ValueError("Invalid ID")

    if not (_validate_phone(caller_phone) and _validate_phone(receiver_phone)):
        raise ValueError("Invalid phone")


def make_user(user_id: int, fullname: str, phone: str) -> User:
    if phone.startswith(LOCAL_PHONE_PREFIX):
        return LocalUser(user_id, fullname, phone)
    return ForeignUser(user_id, fullname, phone)


@dataclass(slots=True)
class ActiveCall:
    caller: User
    receiver: User

    @property
    def is_cross_border(self) -> bool:
        return type(self.caller) is not type(self.receiver)


class Switchboard:
    def __init__(self) -> None:
        self._active_calls: list[ActiveCall] = []
        self._cross_border_calls: list[ActiveCall] = []

    def register_call(self, raw_call: str) -> ActiveCall:
        if not raw_call.count(',') == 5:
            raise ValueError("Invalid arguments number")

        parts = raw_call.split(",")
        _validate_call_parts(parts)

        caller_id, caller_fullname, caller_phone, receiver_id, receiver_fullname, receiver_phone = parts

        caller = make_user(int(caller_id), caller_fullname, caller_phone)
        receiver = make_user(int(receiver_id), receiver_fullname, receiver_phone)

        call = ActiveCall(caller, receiver)
        self._active_calls.append(call)

        if call.is_cross_border:
            self._cross_border_calls.append(call)

        return call

    def get_active_calls_count(self) -> int:
        return len(self._active_calls)

    def get_cross_border_calls_count(self) -> int:
        return len(self._cross_border_calls)
