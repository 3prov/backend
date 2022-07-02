from django.db import models


class Stage(models.Model):
    """Модель с единственной строкой"""
    class Meta:
        verbose_name = 'Этап'
        verbose_name_plural = 'Этап'

    NO_TASK = 'S1'
    WORK_ACCEPTING = 'S2'
    CHECK_ACCEPTING = 'S3'
    CLOSED_ACCEPT = 'S4'
    STAGES = [
        (NO_TASK, 'Нет задания'),
        (WORK_ACCEPTING, 'Приём работ'),
        (CHECK_ACCEPTING, 'Приём проверок'),
        (CLOSED_ACCEPT, 'Нет приёма работ')
    ]

    stage = models.CharField(
        max_length=2,
        choices=STAGES,
        default=NO_TASK,
        verbose_name='Этап'
    )

    @classmethod
    def object(cls):
        return cls._default_manager.all().first()  # Since only one item

    def save(self, *args, **kwargs):
        self.pk = self.id = 1
        return super().save(*args, **kwargs)

    @staticmethod
    def get_stage() -> dict[str, str]:
        current_stage = Stage.object().stage
        for one_tuple in Stage.STAGES:
            if one_tuple[0] == current_stage:
                return {current_stage: one_tuple[1]}
        raise Exception('List of tuples: Key doesnt exists')

    @staticmethod
    def switch_stage_to_next() -> dict[str, str]:
        current_stage = Stage.object().stage
        iterator = iter(Stage.STAGES * 2)
        while next(iterator)[0] != current_stage:
            continue
        next_stage = next(iterator)
        Stage(stage=next_stage[0]).save()
        return Stage.get_stage()


