# Документация API v1

- /api/v1/docs/
- /api/v1/redoc/
- /api/v1/swagger/


## Создание пользователя
- POST: /api/v1/authtoken/users/ # TODO: убрать `password`
- GET: ... #получить token, uuid пользователя


## Загрузка текста недели
- POST: /api/v1/rus/text/assign/ # TODO: создать сборник текстов 50 штук (в начале уч. года загрузить). позволить пользователям загружать-предлагать свои тексты, в воскресенье проводить опрос-выбор текста недели. проверять тексты пользователей на наличие рекламы/спама
- POST: /api/v1/rus/text/keys/add/


## Смена этапа недели на этап приёма работ (S1 -> S2)
- GET: /api/v1/management/switch_stage_to_next/ # TODO: to celery


## Отправка работы
- POST: /api/v1/rus/essay/create_link_to_form/
- GET: /api/v1/rus/essay/get_user_form_links/<uuid:user>/

- GET: /f/w/{encoded_part}/
  - POST: /api/v1/rus/essay/form-url/<str:encoded_part>/post/
  - GET, PUT, PATCH: /api/v1/rus/essay/detail/<str:encoded_part>/edit/


## Смена этапа недели на этап приёма проверок (S2 -> S3)
> **Warning**:
> Возможно при наличии хотя бы 4 работ

TODO: при переходе на этап S3 необходимо проверить все работы на правильность
- GET: /api/v1/management/switch_stage_to_next/ # TODO: to celery


## Отправка проверок
### Участники недели
- GET: /api/v1/rus/evaluation/get_form_urls/<uuid:user>/ #отправка пользователю трёх работ вместе с ссылками на формы
- GET: /f/e/<str:encoded_part>/
  - POST: /api/v1/rus/evaluation/form-url/<str:encoded_part>/post/
  - GET, PUT, PATCH: /api/v1/rus/evaluation/form-url/<str:encoded_part>/edit/
  - POST: /api/v1/rus/evaluation/sentence_review/form-url/<str:encoded_part>/post/
  - GET, PUT, PATCH: /api/v1/rus/evaluation/sentence_review/form-url/<str:encoded_part>/edit/<int:sentence_number>/
> **Note**:
> После проверки трёх этих работ участник становится волонтёром.

### Волонтеры (не отправляли работы на текущей неделе)
- GET: /api/v1/rus/evaluation/volunteer_get_distribution/<uuid:user>/
- POST: /api/v1/rus/evaluation/volunteer_create_next_and_get_form_urls/<uuid:user>/
- GET: /f/e/<str:encoded_part>/
  - POST: /api/v1/rus/evaluation/form-url/<str:encoded_part>/post/
  - GET, PUT, PATCH: /api/v1/rus/evaluation/form-url/<str:encoded_part>/edit/
  - POST: /api/v1/rus/evaluation/sentence_review/form-url/<str:encoded_part>/post/
  - GET, PUT, PATCH: /api/v1/rus/evaluation/sentence_review/form-url/<str:encoded_part>/edit/<int:sentence_number>/


## Результаты недели
- POST: /api/v1/rus/results/get_link_to_form/<uuid:user>/ # TODO: to celery auto create
- GET: /f/r/<str:encoded_part>/

### Оценка проверок
- POST: /api/v1/rus/results/rate_essay_evaluation/<str:encoded_part>/post/

### Доступно всем результаты всех недель
- GET: /api/v1/rus/results/


#генерация EvaluationFormURL при запросе на проверку
#(чем меньше проверок у работы, тем больше баллов рейтинга нужно начислять проверяющему)
