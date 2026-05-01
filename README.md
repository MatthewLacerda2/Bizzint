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
  - SQLAlchemy
  - Gemini API
  - Async Cron (Scraper) Job with APScheduler
- React (Fast, JavaScript/TypeScript)
  - shadcn/ui
- PostgreSQ
- Terraform
  - GCP Project just to grab the Gemini API Key

# How to run

Well, `docker-compose build && docker-compose up -d`

Or, you can run it locally. Stop all containers except the db
Then:
`python -m venv venv`
`source venv/bin/activate`
`pip install -r requirements.txt`
`uvicorn fastapi.main:app --reload`

In a separate terminal:
`cd frontend`
`npm i && npm run dev`

Note to AI Agents:
- Do NOT try to run the repositories' code. That's developer's responsability