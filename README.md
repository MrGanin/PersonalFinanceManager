💰 Менеджер личных финансов

Django-приложение для учёта доходов и расходов с визуализацией.

🚀 Функционал

- Добавление/просмотр транзакций (доходы/расходы)
- Категории с лимитами
- График расходов по категориям (круговая диаграмма)
- Динамика доходов/расходов по месяцам (линейный график)
- Фильтрация по году

🛠 Стек

- Python 3.11
- Django 5.0
- PostgreSQL
- Bootstrap 5
- Chart.js
- Docker + docker-compose

📦 Быстрый старт

bash
Клонировать репозиторий
git clone https://github.com/yourname/finance-manager.git
cd finance-manager

Запустить контейнеры
docker-compose up --build -d

Применить миграции
docker-compose exec web python manage.py migrate

Создать суперпользователя
docker-compose exec web python manage.py createsuperuser
