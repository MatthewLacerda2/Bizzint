This is Business Intelligence platform, with data analytics and AI.

We have a database of companies. Our Chatbot can read the db and answer questions.
Users can get answers, generate reports, forecast.

We scrape publicly available data.
  - api.opencnpj.org: to search for a specific companies' data
  - econodata.com.br: to search for companies in general

The only hurdle is searching for phone numbers of people within a specific company.
Haven't solved that one out.

# Tech stack

- FastAPI (Fast, Python)
  - Alembic/SQLAlchemy
  - Gemini API
- React (Fast, JavaScript/TypeScript)
  - shadcn/ui
- PostgreSQL

# How to run

`docker-compose build && docker-compose up -d`
`alembic upgrade head`

Or, you can run it locally:
`python -m venv venv`
`source venv/bin/activate`
`pip install -r requirements.txt`
`uvicorn app.main:app --reload`

In a separate terminal:
`cd frontend`
`npm i && npm run dev`