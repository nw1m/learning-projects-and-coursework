# Структура events.csv

| Поле | Описание |
|---|---|
| `event_id` | Уникальный номер события |
| `session_id` | Идентификатор сессии |
| `user_id` | Учебный идентификатор пользователя |
| `event_name` | Тип события: visit, view_product, add_to_cart, checkout или purchase |
| `event_time` | Дата и время события |
| `device` | Устройство: mobile, desktop или tablet |
| `source` | Источник: organic, paid_ads, email или referral |

Одна сессия содержит от одного до пяти событий. Данные искусственные.
