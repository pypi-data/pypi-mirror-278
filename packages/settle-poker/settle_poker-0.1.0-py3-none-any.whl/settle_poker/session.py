from dataclasses import dataclass
from typing import Iterator

from .solver import solve_poker_settlement


@dataclass
class Transaction:
    sender: str
    receiver: str
    amount: int


class Session:
    def __init__(self):
        self._balances = {}

    def add_user(self, user: str):
        if user in self._balances:
            raise ValueError('User already exists')
        self._balances[user] = 0

    def add_buy_in(self, user, amount: int):
        if user not in self._balances:
            raise ValueError('Invalid user')
        self._balances[user] -= amount

    def cash_out(self, user: str, amount: int):
        if user not in self._balances:
            raise ValueError('Invalid user')
        self._balances[user] += amount

    def settle(self) -> Iterator[Transaction]:
        balances = list(self._balances.values())
        assert sum(balances) == 0

        transactions = solve_poker_settlement(balances)
        users = list(self._balances.keys())

        for transaction in transactions:
            yield Transaction(users[transaction[1]], users[transaction[0]], transactions[transaction])