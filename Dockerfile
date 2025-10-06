FROM python:3.10-slim

WORKDIR /app

RUN pip install pipenv

COPY data/rag_dataset.csv data/rag_dataset.csv
COPY ["Pipfile", "Pipfile.lock", "./"]

RUN pipenv install --deploy --ignore-pipfile --system

COPY pawfect-mate .

EXPOSE 5000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "5000", "--reload"]