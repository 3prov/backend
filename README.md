# Документация API v1


## Запуск репозитория
1. Создание `.env` файла
```bash
cp .env.example .env
vim .env
```
2. Создание `.env.db` файла (для режима **prod**)
```bash
cp .env.db.example .env.db
vim .env.db
```
3. Запуск
- в режиме **dev**
```bash
make dev
```
- в режиме **prod**
```bash
make prod
```
4. Очистка `containers`, `images` (после запуска в режиме **dev**)
```bash
make clean_dev
```
5. Очистка `volumes` (после запуска в режиме **dev**)
```bash
make fclean_dev
```

---

## Документация

- docs/
- redoc/
- swagger/

- [Frontend](/README_frontend.md)
- [Bot](/README_bot.md)


> **Warning**:
> Информация ниже в настоящем файле временная и неактуальна.


### Создание пользователя
- POST: authtoken/users/ # TODO: убрать `password`
- GET: ... #получить token, uuid пользователя


### Загрузка текста недели
- POST: rus/text/assign/ # TODO: создать сборник текстов 50 штук (в начале уч. года загрузить). позволить пользователям загружать-предлагать свои тексты, в воскресенье проводить опрос-выбор текста недели. проверять тексты пользователей на наличие рекламы/спама
- POST: rus/text/keys/add/


### Смена этапа недели на этап приёма работ (S1 -> S2)
- GET: control/switch_stage_to_next/ # TODO: to celery beat


### Отправка работы
- POST: rus/essay/create_link_to_form/
- GET: rus/essay/get_user_form_links/`uuid:user`/

- GET: encoded-form-urls/work/`str:encoded_part`/
  - POST: rus/essay/form-url/`str:encoded_part`/post/
  - GET, PUT, PATCH: rus/essay/detail/`str:encoded_part`/edit/


### Смена этапа недели на этап приёма проверок (S2 -> S3)
> **Warning**:
> Возможно при наличии хотя бы 4 работ

TODO: при переходе на этап S3 необходимо проверить все работы на правильность
- GET: control/switch_stage_to_next/


### Отправка проверок
#### Участники недели
- GET: rus/evaluation/get_form_urls/`uuid:user`/ #отправка пользователю трёх работ вместе с ссылками на формы
- GET: encoded-form-urls/evaluation/`str:encoded_part`/
  - POST: rus/evaluation/form-url/`str:encoded_part`/post/
  - GET, PUT, PATCH: rus/evaluation/form-url/`str:encoded_part`/edit/
  - POST: rus/evaluation/sentence_review/form-url/`str:encoded_part`/post/
  - GET, PUT, PATCH: rus/evaluation/sentence_review/form-url/`str:encoded_part`/edit/`int:sentence_number`/
> **Note**:
> После проверки трёх этих работ участник становится волонтёром.

#### Волонтеры (не отправляли работы на текущей неделе)
- GET: rus/evaluation/volunteer_get_distribution/`uuid:user`/
- POST: rus/evaluation/volunteer_create_next_and_get_form_urls/`uuid:user`/
- GET: encoded-form-urls/evaluation/`str:encoded_part`/
  - POST: rus/evaluation/form-url/`str:encoded_part`/post/
  - GET, PUT, PATCH: rus/evaluation/form-url/`str:encoded_part`/edit/
  - POST: rus/evaluation/sentence_review/form-url/`str:encoded_part`/post/
  - GET, PUT, PATCH: rus/evaluation/sentence_review/form-url/`str:encoded_part`/edit/`int:sentence_number`/


### Результаты недели
- POST: rus/results/get_link_to_form/`uuid:user`/ # TODO: to celery beat
- GET: encoded-form-urls/results/`str:encoded_part`/

#### Получение текста недели по ссылке на результаты
- GET: rus/text/get_text_by_results_form_url/`str:encoded_part`/

#### Оценка проверок
- POST: rus/results/rate_essay_evaluation/`str:encoded_part`/post/

#### Доступно всем результаты всех недель
- GET: rus/results/


#генерация EvaluationFormURL при запросе на проверку
#(чем меньше проверок у работы, тем больше баллов рейтинга нужно начислять проверяющему)
