# innovation-portfolio-optimizer
Описание: оптимизатор R&amp;D-портфеля. Real Options Valuation, BCG-матрица, эффективная граница, симуляция Монте-Карло, рекомендации совету директоров.  Стек: Python, FastAPI, PostgreSQL, SciPy, Streamlit, Docker.

# innovation-portfolio-optimizer

Оптимизатор R&D-портфеля с Real Options, BCG-матрицей и эффективной границей.

## Возможности
- Real Options Valuation (ROV) с дисконтированием
- BCG-матрица (звёзды, дойные коровы, вопросы, собаки)
- Жадный оптимизатор с бюджетом и лимитом риска
- Эффективная граница портфелей (Монте-Карло)
- Стресс-тест на провал high-risk проектов
- Streamlit-дашборд

## Быстрый старт

cp .env.example .env
docker-compose up --build

API: http://localhost:8000/docs
Dashboard: http://localhost:8501

## Пример

curl -X POST http://localhost:8000/api/projects \
  -H "Content-Type: application/json" \
  -d '{"code":"P1","name":"AI Assistant","investment_m":15,
       "expected_return_m":80,"probability_success":0.5,
       "time_to_market_y":2,"risk_class":"medium","strategic_fit":0.8}'

curl -X POST http://localhost:8000/api/optimize \
  -H "Content-Type: application/json" \
  -d '{"budget":100,"max_high_risk_share":0.3}'

## Тесты

pytest tests/ -v

## Лицензия
MIT
