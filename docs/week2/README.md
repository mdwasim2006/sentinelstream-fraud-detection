\# Week 2 – Core Transaction Pipeline



\## Objective

Build the core transaction ingestion pipeline capable of processing

transactions in real time with validation, idempotency, and risk scoring.



\## Key Features Implemented

\- POST /transaction API endpoint

\- Request validation using Pydantic

\- Idempotency handling to prevent duplicate transactions

\- Basic fraud risk evaluation logic

\- PostgreSQL integration using SQLAlchemy (async)

\- API documentation via Swagger (FastAPI)



\## Sample Test

\- Duplicate transaction returns status: DUPLICATE

\- High-risk transaction returns status: HIGH\_RISK

\- Normal transaction returns status: APPROVED



\## Tech Stack

\- FastAPI

\- PostgreSQL

\- SQLAlchemy (async)

\- Uvicorn



\## Status

Week 2 objectives completed and verified locally.



