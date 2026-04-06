from __future__ import annotations

from dataclasses import dataclass

from app.users import User, ForeignUser, LocalUser


LOCAL_PHONE_PREFIX = "+7"


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
        caller_id, caller_fullname, caller_phone, receiver_id, receiver_fullname, receiver_phone = raw_call.split(",")

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
