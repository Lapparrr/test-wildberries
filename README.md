
\
## Quickstart

### 2. Install dependecies with [Poetry](https://python-poetry.org/docs/)

```bash
cd your_project_name

### Poetry install (python3.12)
poetry install
```

Note, be sure to use `python3.12` with this template with either poetry or standard venv & pip, if you need to stick to some earlier python version, you should adapt it yourself (remove new versions specific syntax for example `str | int` for python < 3.10)

### 3. Setup database and migrations

```bash
### Setup database
docker-compose up -d

### Run Alembic migrations
alembic upgrade head
```

### 4. Now you can run app

```bash
### And this is it:
uvicorn app.main:app --reload

```


### 5. Запуск тестов
```bash
pytest
```

### 5. Планирование архитектуры 
	Текущая архитектура проекта позволяет быстро добавлять функционал
	1. Просмотр чужой ленты - добавление endpoint c условием сортировки по пользователям
	2. Публичность воспоминаний - Данная реализация подразумевает добавление к воспоминаниям флага публичность 
	и изменение ендпоинта поиска остальных воспоминанием с добавлением условия, чтобы флаг был публичным
	3. Анонимные воспоминания - Добавление флага анонимности к воспоминанием. Необходимо добавить проверку, 
	чтобы при выводе в ендпоинте заменять user_id - на uuid анонимного пользователя
	4. Создание новой таблицы в БД friends со связями Many-to-Many. Создание ручек добавление в друзья/ удаления и просмотра
	5. Лента только друзей - создание ручек для вывода постов согласно условию соотвествия в 


	