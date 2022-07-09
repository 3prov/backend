## Создание пользователя
- POST: /api/v1/authtoken/users/
- GET: ... #получить token, uuid пользователя


## Отправка работы
- POST: /api/v1/rus/essay/create_link_to_form/ (user_uuid)
- GET: /api/v1/rus/essay/get_user_form_links/<uuid:user>/

- GET: /f/w/{encoded_part}/
  - POST: /api/v1/rus/essay/form-url/<str:encoded_part>/post/
  - GET, PUT, PATCH: /api/v1/rus/essay/detail/{str:endoded_part}/edit/


## Отправка проверок
1. Участники недели
  - GET: /api/v1/rus/evaluation/get_form_urls/<uuid:user>/ #отправка пользователю трёх работ вместе с ссылками на формы
  - GET: /f/e/<str:encoded_part>/
    - POST: /api/v1/rus/evaluation/form-url/<str:encoded_part>/post/
    - GET, PUT, PATCH: /api/v1/rus/evaluation/form-url/<str:encoded_part>/edit/
    - POST: /api/v1/rus/evaluation/sentence_review/
  #после проверки трёх этих работ участник становится волонтёром


2. Волонтеры
  - POST: /api/v1/rus/evaluation/get_link_to_form/ (user_uuid)
  - GET: /f/e/<str:endoded_part>


  #отображение всех работ через Бота
  #генерация EvaluationFormURL при запросе на проверку
  #(чем меньше проверок у работы, тем больше баллов рейтинга нужно начислять проверяющему)
