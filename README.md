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

🧪 Запуск тестов
docker-compose exec web python manage.py test -v 2

📁 Структура
core/
├── models.py      # Категории и транзакции
├── views.py       # Логика + агрегации
├── forms.py       # Форма транзакции
└── templates/     # Шаблоны с графиками
