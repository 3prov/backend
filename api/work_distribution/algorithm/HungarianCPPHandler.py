import os.path
from typing import NamedTuple

from api.models import User


class HungarianCPPAlgorithm:

    def __init__(self):
        __base_dir = os.path.dirname(os.path.abspath(__file__))
        self._path_to_cpp_library = os.path.join(__base_dir, ...)

    @staticmethod
    def _create_first_matrix(users_ratings: list[int]) -> list:
        """
        Создание матрицы для первого распределения (с наименьшей разницей в рейтинге).
        """
        matrix = []
        for i in range(len(users_ratings)):
            tmp = []
            for j in range(len(users_ratings)):
                if i == j:  # проверка, чтобы своя же работа не могла попасться
                    tmp.append(2147483647)
                else:
                    tmp.append(round(abs(users_ratings[i] - users_ratings[j]), 2))
            matrix.append(tmp)
        return matrix

    @staticmethod
    def _create_matrix_with_pair_blocks(users_ratings: list[int], pairs_to_block: list, old_matrix: list) -> list:
        """
        Создание матрицы для N распределения (с наименьшей разницей в рейтинге).
        """
        matrix = []
        for i in range(len(users_ratings)):
            tmp = []
            for j in range(len(users_ratings)):
                # проверка, чтобы одно сочинение не выдалось больше одного раза
                if i == j or (i, j) in pairs_to_block or 2147483647 == old_matrix[i][j]:
                    tmp.append(2147483647)
                else:
                    tmp.append(round(abs(users_ratings[i] - users_ratings[j]), 2))
            matrix.append(tmp)
        return matrix

    class ResultPair(NamedTuple):
        evaluator: User
        work_author: User

    def make_necessary_distribution_for_week_participants(self, participants: set) -> set[ResultPair]:
        """
        Создание распределения для участников недели.
        """
        # cost_matrix = [
        #     [4, 2, 8],
        #     [4, 3, 7],
        #     [3, 1, 6]
        # ]
        # print("Calculated value:\t", hungarian.get_total_potential())  # = 12
        # print("Expected results:\n\t[(0, 1), (1, 0), (2, 2)]")
        return

