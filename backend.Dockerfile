FROM python:3.12-slim

WORKDIR /app

COPY backend/Pipfile* ./
RUN pip install pipenv && \
    pipenv install --system --deploy

COPY backend/ .

EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
