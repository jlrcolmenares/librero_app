FROM python:3.11-slim

WORKDIR /app

COPY Pipfile* ./
RUN pip install pipenv && \
    pipenv install --system --deploy

COPY . .

EXPOSE 8000

CMD ["uvicorn", "web.app:app", "--host", "0.0.0.0", "--port", "8000"]
