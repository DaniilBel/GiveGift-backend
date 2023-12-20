# Give gifts

## Запуск проекта

1. Установить все зависимости из `requirements.txt` при помощи команды: `pip install -r requirements.txt`.
2. Запустить проект при помощи команды: `python main.py`

## Протокол общения с сервером

Система использует аккаунты пользователей с некоторыми
заданными атрибутами _(далее по контексту будет ясно, какие именно
атрибуты относятся к пользователям)_.

Также хранятся предпочтения, которые представляют собой предпочтения
из предложенного набора _(считаем,
что модификация Администратором предпочтений не затрагивает
уже имеющиеся у пользователей)_.

### Некоторые запросы содержат:

* `jwt_required optional` -
  требуется указать _**bearer token**_, иначе **не вся функциональность
  будет доступна** _(назовём имеющего токен пользователя авторизованным)_
* `jwt_required` - **функция с данным декоратором доступна только авторизованным пользователям.**

По умолчанию, любая такая функция обязана проверять актуальность переданного токена:

* При выходе пользователя его токен становится **неактуальным**
* Токен также может физически **устареть**, необходимо поддержать его обновление (автоматическая подмена "почти"
  устаревших токенов, моложе 1 часа, но старше 30 минут предусмотрена, **смотрите на ответ сервера, если в нём
  содержится `access_token`,
  то необходимо обновить токен у себя**).

## Описание методов API

### Register

* ### `/register`, `POST` `jwt_required optional`
  _Регистрация пользователя_

  #### Входные данные
    ``` json
    {
        "nickname": "...",
        "email": "...",
        "password": "...",
        "birth_date": "...",
        "about": "...",
        "interests": "[...]"
    }
    ```
  **Required: `nickname`, `email`, `password`**
    * Адрес электронной почты должен быть уникален
    * Пароль должен содержать прописные и строчные буквы латинского алфавита, цифры и состоять не менее чем из
      восьми символов

  #### Вывод
  _Сообщение об успешной регистрации, иначе сообщение об ошибке_

### Login

* ### `/login`, `POST` `jwt_required optional`
  _Вход пользователя. Если токен не является актуальным, то происходит его обновление,
  в противном случае, если пользователь не вышел из системы,
  ошибка "Token is actual", 401_

  #### Входные данные
    ``` json
     {
        "email":"...",
        "password":"..."
     }
   ```
  **Required: `email`, `password`**

  #### Вывод
  _Сообщение об успешном входе, иначе сообщение об ошибке_

### Logout

* ### `/logout`, `POST` `jwt_required`
  _Выход пользователя_

### Account

* ### `/account`, `GET` `jwt_required`
  _Вывод данных о своем аккаунте_
  #### Вывод
    ``` json
    {
        "id": "...",
        "nickname": "...",
        "email": "...",
        "about": "...",
        "birth_date": "...",
        "interests": "[...]",
        "friends": "[...]"
    }
    ```

*  ### `/account`, `POST` `jwt_required`
   _Изменение данных о своем аккаунте_
   #### Входные данные
   ``` json
    {
        "id": "...",
        "nickname": "...",
        "email": "...",
        "about": "...",
        "birth_date": "...",
        "interests": "[...]"
    }
   ```
   #### Вывод
   _Сообщение об успешном изменении данных, иначе сообщение об ошибке_

* ### `/get_user_info/:id`, `GET` `jwt_required optional`
  _Получение информации о пользователе по id_
    * В случае `id = 0` выдается информация о себе _(аналогично `/account`)_, `jwt_required`
    * Иначе выдается информация о пользователе по указанному `id`

  #### Вывод
  ``` json
  {
      "id": "...",
      "nickname": "...",
      "email": "...",
      "about": "...",
      "birth_date": "...",
      "interests": "[...]",
      "friends": "[...]",
      "is_me": "true/false"
  }
  ```

### Friends - все методы `jwt_required`

* ### `/friends`, `GET`
  _Получение списка друзей, входящих/исходящих заявок_

  #### Вывод
    ``` json
  {
        "friends": "[...]"
        "incoming_requests": "[...]"
        "outgoing_requests": "[...]"
  }
    ```

* ### `/friends`, `DELETE`
  _Удаление друга по `id` из списка друзей_
  #### Входные данные
    ``` json
  {
        "friend_id": "..."
  }
    ```

* ### `/outgoing_friend_request`, `DELETE`
  _Отзывает заявку человеку с указанным `id`_
  #### Входные данные
    ``` json
  {
        "friend_id": "..."
  }
    ```

* ### `/outgoing_friend_request`, `POST`
  _Отправляет заявку человеку с указанным `id`_
  #### Входные данные
    ``` json
  {
        "friend_id": "..."
  }
    ```

* ### `/incoming_friend_request` `DELETE`
  _Отклоняет входящую заявку от человека с указанным `id`_
  #### Входные данные
    ``` json
  {
        "friend_id": "..."
  }
    ```
* ### `/incoming_friend_request` `POST`
  _Принимает входящую заявку от человека с указанным `id`_

  #### Входные данные
    ``` json
  {
        "friend_id": "..."
  }
    ```

### Generate ideas

* ### `/generate_ideas`, `POST` `jwt_required optional`

  _Генерация идей подарков_

  #### Входные данные
    * Если генерация идей для друга (`jwt_required`):
      ``` json
      {
          "friend_id": "..."
      }
      ```
    * Иначе:
      ``` json
      {
          "interests": "[...]",
          "price_range": "[start_price, end_price]"
      }
      ```
        * `interests` - список интересов
        * `price_range` - диапазон цен для подарка
  #### Вывод
  _В случае успешного выполнения, список идей следующего формата:_
  ``` json
    [
        {
          "title": "...",
          "img_link": "...",
          "market_link": "..."
        }, ...
    ]
    ```
    * `title` - сама идея
    * `img_link` - фотография идеи подарка
    * `market_link` - ссылка на нее


### Interests
* ### `/get_all_interests`, `GET`
  
  _Получить список всех интересов_
  #### Вывод:
   ``` json
      {
          "all_interests": "[...]"
      }
  ```

### Admin - все методы `jwt_required`

Здесь находятся **методы, доступные только администраторам**.

Выполняется 
проверка на email == 'ADMIN@ADMIN.su', может существовать
только один аккаунт с таким email, в тестовой версии 
создать его может любой


* ### `/edit_interests`, `POST`
  _Изменение списка интересов_
    
  #### Входные данные
    ``` json
    {
        "new_interests": "[...]",
        "edit_interests": "[{'interest_name': '...', 'new_name': '...'}, ...]"
    }
    ```
    * `new_interests` - список из строк, новые предпочтения не должны совпадать ни с одним из старых
    * `edit_interests` - список из объектов
      * `interest_name`: уже существующий интерес, который нужно изменить
      * `new_name`: на что нужно изменить интерес под названием `interest_name`
