FROM python:3.11

WORKDIR /app

COPY ./src/api /app/src/api

RUN pip install -r ./src/api/requirements.txt

ENV PYTHONPATH=/app/src

CMD ["fastapi", "run", "./src/api/main.py", "--port", "5000"]