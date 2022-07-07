from api.models import User
from api.rus.evaluations.models import EssayEvaluation
from api.work_distribution.algorithm.structures import ResultPair
from django.db.models.query import QuerySet


class SortByRatingAlgorithm:

    @staticmethod
    def make_optionally_distribution_for_volunteer(
            volunteer: User,
            participants: list[User],
            existing_evaluations_of_works: QuerySet[EssayEvaluation]
    ) -> list[ResultPair]:
        """
        Создание необязательного распределения для одного человека.
        """

        users_and_rating_difference = []
        for participant in participants:
            users_and_rating_difference.append({
                'participant': participant,
                'rating_difference': abs(volunteer.rating - participant.rating),
                'existing_evaluations_of_works': existing_evaluations_of_works.filter(work__author=participant).count()
            })

        sorted_users_and_rating_difference = sorted(
            users_and_rating_difference,
            key=lambda d: (d['existing_evaluations_of_works'], d['rating_difference'])
        )

        result: list[ResultPair] = []
        for participant in sorted_users_and_rating_difference:
            result.append(ResultPair(evaluator=volunteer, work_author=participant['participant']))

        return result
