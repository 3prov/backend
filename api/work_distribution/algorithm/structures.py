from typing import NamedTuple

from api.models import User


class ResultPair(NamedTuple):
    evaluator: User
    work_author: User


class OneDistribution(NamedTuple):
    pairs: list[tuple[int, int]]
    cost: float
