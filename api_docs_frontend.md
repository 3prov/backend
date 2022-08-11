# Документация API v1 для фронтенда

> **Note**:
> `str:encoded_part` - это 16-ти символьная (пример: 84e53cab68407098) уникальная для кажного участника строка, которая позволяет отправлять работы, проверки и просматривать результаты недели без аутентификации на сайте.

> **Note**:
> При выводе списков используется пагинация. По умолчанию размер одной страницы - 50 элементов. Для доступа к следующей группе элементов надо делать запрос по ключу `next`.


## Отправка сочинения
### encoded-form-urls/work/`str:encoded_part`/
#### GET
Возвращает данные о тексте неделе, статусе отправки работы, ссылки на отправку и изменение работы.
```json
{
  "work_already_sent": true,
  "urls": {
    "to_POST": false,
    "to_PATCH": "/api/v1/rus/essay/form-url/84e53cab68407098/edit/"
  },
  "work": {
    "essay": {
      "body": "test5",
      "created_at": "2022-08-09T02:50:46.335684+03:00"
    }
  },
  "task": {
    "week_id": {
      "study_year_from": 2022,
      "study_year_to": 2023,
      "week_number": 2
    },
    "body": "Ничто так не мешает улучшению жизни людей, как то, что они хотят...",
    "author": "(по Л. Толстому)",
    "author_description": "Лев Николаевич Толстой — один из наиболее известных русских писателей и мыслителей, один из величайших писателей-романистов мира."
  }
}
```

### rus/essay/form-url/`str:encoded_part`/post/
#### POST
Отправляет сочинение используя лишь `str:encoded_part` и тело сочинения.
- Запрос:
```json
{
    "body": "Что движет солдатами, которые готовы добровольно пожертвовать своей жизнью? Эту проблему рассматривает Л.А. Кассиль в предложенном для анализа тексте. Размышляя..."
}
```

- Ответ:
```json
{
  "created_at": "2022-08-11T01:12:36.807958+03:00",
  "body": "Что движет солдатами, которые готовы добровольно пожертвовать своей жизнью? Эту проблему рассматривает Л.А. Кассиль в предложенном для анализа тексте. Размышляя..."
}

```

### rus/essay/form-url/`str:encoded_part`/edit/
#### PUT, PATCH
Изменяет сочинение.
- Запрос:
```json
{
    "body": "Какой поступок можно назвать подвигом? Ответ на этот вопрос можно найти в предложенном для анализа тексте. Рассмотрим эпизод..."
}
```

- Ответ:
```json
{
  "created_at": "2022-08-11T01:12:36.807958+03:00",
  "body": "Какой поступок можно назвать подвигом? Ответ на этот вопрос можно найти в предложенном для анализа тексте. Рассмотрим эпизод..."
}
```

## Отправка проверки
### /encoded-form-urls/evaluation/`str:encoded_part`/
#### GET
Возвращает данные о тексте неделе, статусе отправки проверки, ссылки на отправку и изменение проверки, список комментариев к предложениям.
```json
{
  "evaluation_already_sent": true,
  "urls": {
    "to_POST": false,
    "to_PATCH": "/api/v1/rus/evaluation/form-url/688821ee554669b5/edit/"
  },
  "evaluation": {
    "criteria": {
      "id": "30476e11-db08-4762-a133-83736e7a50a8",
      "k1": 1,
      "k2": 4,
      "k3": 1,
      "k4": 1,
      "k5": 1,
      "k6": 1,
      "k7": 1,
      "k8": 0,
      "k9": 0,
      "k10": 1,
      "k11": 1,
      "k12": 1
    },
    "created_at": "2022-08-11T01:42:30.903396+03:00",
    "sentences_review": [
      {
        "sentence_number": 1,
        "evaluator_comment": "Пропустил 4 запятых",
        "mistake_type": "K08"
      }
    ]
  },
  "task": {
    "week_id": {
      "study_year_from": 2022,
      "study_year_to": 2023,
      "week_number": 2
    },
    "body": "Ничто так не мешает улучшению жизни людей, как то, что они хотят...",
    "author": "(по Л. Толстому)",
    "author_description": "Лев Николаевич Толстой — один из наиболее известных русских писателей и мыслителей, один из величайших писателей-романистов мира."
  }
}
```

### /api/v1/rus/evaluation/form-url/`str:encoded_part`/post/
#### POST
Отправляет проверку по критериям.
- Запрос:
```json
{
    "criteria": {
        "k1": 1,
        "k2": 4,
        "k3": 1,
        "k4": 1,
        "k5": 1,
        "k6": 1,
        "k7": 1,
        "k8": 0,
        "k9": 0,
        "k10": 1,
        "k11": 1,
        "k12": 1
    }
}
```

- Ответ:
```json
{
  "criteria": {
    "id": "30476e11-db08-4762-a133-83736e7a50a8",
    "k1": 1,
    "k2": 4,
    "k3": 1,
    "k4": 1,
    "k5": 1,
    "k6": 1,
    "k7": 1,
    "k8": 0,
    "k9": 0,
    "k10": 1,
    "k11": 1,
    "k12": 1
  },
  "created_at": "2022-08-11T02:14:20.190380+03:00",
  "sentences_review": [
    {
      "sentence_number": 1,
      "evaluator_comment": "Пропустил 5 запятых!!!!!!",
      "mistake_type": "K08"
    }
  ]
}
```

### /api/v1/rus/evaluation/form-url/`str:encoded_part`/edit/
#### PUT, PATCH
Изменяет проверку по критериям.
- Запрос:
```json
{
    "criteria": {
        "k1": 0,
        "k2": 5,
        "k3": 0,
        "k4": 0,
        "k5": 0,
        "k6": 0,
        "k7": 1,
        "k8": 0,
        "k9": 0,
        "k10": 1,
        "k11": 1,
        "k12": 1
    }
}
```

- Ответ:
```json
{
  "criteria": {
    "id": "30476e11-db08-4762-a133-83736e7a50a8",
    "k1": 0,
    "k2": 5,
    "k3": 0,
    "k4": 0,
    "k5": 0,
    "k6": 0,
    "k7": 1,
    "k8": 0,
    "k9": 0,
    "k10": 1,
    "k11": 1,
    "k12": 1
  },
  "created_at": "2022-08-11T01:42:30.903396+03:00",
  "sentences_review": [
    {
      "sentence_number": 1,
      "evaluator_comment": "Пропустил 5 запятых!!!!!!",
      "mistake_type": "K08"
    }
  ]
}
```


### rus/evaluation/sentence_review/form-url/`str:encoded_part`/post/
#### POST
Отправляет проверку одного предложения.
- Запрос:
```json
{
    "sentence_number": 1,
    "evaluator_comment": "Пропустил 4 запятых",
    "mistake_type": "K08"
}
```

- Ответ:
```json
{
    "sentence_number": 1,
    "evaluator_comment": "Пропустил 4 запятых",
    "mistake_type": "K08"
}
```

### rus/evaluation/sentence_review/form-url/`str:encoded_part`/edit/`int:sentence_number`
#### PUT, PATCH
Изменяет проверку одного предложения.
- Запрос:
```json
{
    "evaluator_comment": "Пропустил 5 запятых!!!!!!",
    "mistake_type": "K08"
}
```

- Ответ:
```json
{
  "sentence_number": 1,
  "evaluator_comment": "Пропустил 5 запятых!!!!!!",
  "mistake_type": "K08"
}
```


## Просмотр результатов недели
### encoded-form-urls/results/`str:encoded_part`/
#### GET
Возвращает списка проверок.
```json
[
  {
    "criteria": {
      "id": "30476e11-db08-4762-a133-83736e7a50a8",
      "k1": 0,
      "k2": 5,
      "k3": 0,
      "k4": 0,
      "k5": 0,
      "k6": 0,
      "k7": 1,
      "k8": 0,
      "k9": 0,
      "k10": 1,
      "k11": 1,
      "k12": 1
    },
    "created_at": "2022-08-11T02:14:20.190380+03:00",
    "sentences_review": [
      {
        "sentence_number": 1,
        "evaluator_comment": "Пропустил 5 запятых!!!!!!",
        "mistake_type": "K08"
      }
    ]
  }
]
```

### rus/text/get_text_by_results_form_url/`str:encoded_part`/
#### GET
Возвращает текста по ссылке на результаты недели.
```json
{
    "week_id": {
        "study_year_from": 2022,
        "study_year_to": 2023,
        "week_number": 2
    },
    "body": "Ничто так не мешает улучшению жизни людей, как то, что они хотят...",
    "author": "(по Л. Толстому)",
    "author_description": "Лев Николаевич Толстой — один из наиболее известных русских писателей и мыслителей, один из величайших писателей-романистов мира."
}
```

### rus/results/rate_essay_evaluation/`str:encoded_part`/post/
#### POST
Оценка проверки (звёзды от 1 до 5 включительно).

> **Note:**
> Изменение (PUT, PATCH) не поддерживается, поскульку при POST рейтинг проверяющего изменяется перманентно.
- Запрос:
```json
{
    "score": 4,
    "evaluation_criteria": "30476e11-db08-4762-a133-83736e7a50a8"
}
```

- Ответ:
```json
{
  "score": 4,
  "evaluation_criteria": "30476e11-db08-4762-a133-83736e7a50a8"
}
```

## Просмотр работ за всё время
### rus/results/
#### GET
Возвращает список всех сочинений с их баллами, полученных на проверках.
Доступны query-параметры для фильтрации:
- `task__week_id__study_year_from` - учебный год
- `task__week_id__week_number` - номер недели
```json
{
  "count": 4,
  "next": null,
  "previous": null,
  "results": [
    {
      "week_id": "2022-2023_01",
      "body": "essay1_full_body",
      "evaluations": []
    },
    {
      "week_id": "2022-2023_01",
      "body": "essay2_full_body",
      "evaluations": [
        {
          "criteria_score": 14
        },
        {
          "criteria_score": 20
        }
      ]
    },
    {
      "week_id": "2022-2023_01",
      "body": "essay3_full_body",
      "evaluations": []
    },
    {
      "week_id": "2022-2023_01",
      "body": "essay4_full_body",
      "evaluations": []
    }
  ]
}
```

### rus/text/list_all/
#### GET
Возвращает список всех текстов и номеров недель.
```json
{
  "count": 2,
  "next": null,
  "previous": null,
  "results": [
    {
      "week_id": {
        "study_year_from": 2022,
        "study_year_to": 2023,
        "week_number": 2
      },
      "author": "(по Л. Толстому)"
    },
    {
      "week_id": {
        "study_year_from": 2022,
        "study_year_to": 2023,
        "week_number": 1
      },
      "author": "text1"
    }
  ]
}
```
