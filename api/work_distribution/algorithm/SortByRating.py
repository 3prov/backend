from api.models import User
from api.rus.models import Essay
from api.work_distribution.algorithm.structures import ResultPair
from django.db.models.query import QuerySet


class SortByRatingAlgorithm:

    @staticmethod
    def make_optionally_distribution_for_volunteer(
            volunteer: User,
            participants: list[User],
            existing_week_works: QuerySet[Essay]
    ) -> set[ResultPair]:
        """
        Создание необязательного распределения для одного человека.
        """

        users_and_rating_difference = []
        for participant in participants:
            users_and_rating_difference.append({
                'participant': participant,
                'rating_difference': abs(volunteer.rating - participant.rating),
                'participant_work_check_count': existing_week_works.filter(author=participant).count()
            })

        sorted_users_and_rating_difference = sorted(
            users_and_rating_difference,
            key=lambda d: (d['participant_work_check_count'], d['rating_difference'])
        )

        result = set()
        for participant in sorted_users_and_rating_difference:
            result.add(ResultPair(evaluator=volunteer, work_author=participant['participant']))

        return result
