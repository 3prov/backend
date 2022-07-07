from .mcximings_HungarianAlgorithm import HungarianAlgorithm

from api.models import User
from .structures import ResultPair, OneDistribution


class HungarianCPPAlgorithm:

    def __init__(self):
        self._HungarianLibrary = HungarianAlgorithm()
        self._blocking_value = 2147483647

    def _create_first_matrix(self, users_ratings: list[int]) -> list[list[int]]:
        """
        Создание матрицы для первого распределения (с наименьшей разницей в рейтинге).
        """
        matrix = []
        for i in range(len(users_ratings)):
            tmp = []
            for j in range(len(users_ratings)):
                if i == j:  # проверка, чтобы своя же работа не могла попасться
                    tmp.append(self._blocking_value)
                else:
                    tmp.append(round(abs(users_ratings[i] - users_ratings[j]), 2))
            matrix.append(tmp)
        return matrix

    def _create_matrix_with_pair_blocks(
            self,
            users_ratings: list[int],
            pairs_to_block: list[tuple[int, int]],
            old_matrix: list[list[int]]
    ) -> list[list[int]]:
        """
        Создание матрицы для N распределения (с наименьшей разницей в рейтинге).
        """
        matrix = []
        for i in range(len(users_ratings)):
            tmp = []
            for j in range(len(users_ratings)):
                # проверка, чтобы одна работа не выдалось больше одного раза одному проверяющему
                if i == j or (i, j) in pairs_to_block or self._blocking_value == old_matrix[i][j]:
                    tmp.append(self._blocking_value)
                else:
                    tmp.append(round(abs(users_ratings[i] - users_ratings[j]), 2))
            matrix.append(tmp)
        return matrix

    def _make_distribution_and_append_result(
            self,
            participants: list[User],
            matrix: list[list[int]],
            result: list[ResultPair]
    ) -> OneDistribution:
        distribution = OneDistribution(
            pairs=self._HungarianLibrary.Solve(matrix),
            cost=self._HungarianLibrary.cost
        )
        if distribution.cost >= self._blocking_value:
            print(f'ERROR: {distribution.cost=} too big!')  # TODO: to logger
        # print(f'{distribution=}')  # TODO: to logger?
        for pair in distribution.pairs:
            result.append(ResultPair(evaluator=participants[pair[0]], work_author=participants[pair[1]]))
        return distribution

    def make_necessary_distribution_for_week_participants(self, participants: list[User]) -> list[ResultPair]:
        """
        Создание распределения для участников недели.
        """
        ratings = []
        for participant in participants:
            ratings.append(participant.rating)

        result: list[ResultPair] = []

        matrix = self._create_first_matrix(ratings)
        distribution = self._make_distribution_and_append_result(participants, matrix, result)
        for i in range(1, len(participants) - 1):
            print(f"распределение #{i}")  # TODO: to logger
            # print(f'{matrix=}')  # TODO: to logger?
            matrix = self._create_matrix_with_pair_blocks(ratings, distribution.pairs, matrix)
            distribution = self._make_distribution_and_append_result(participants, matrix, result)

        return result
