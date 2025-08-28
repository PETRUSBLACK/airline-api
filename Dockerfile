FROM python:3.11-slim

WORKDIR /app

# copy your project
COPY . /app

# install dependencies
RUN pip install --no-cache-dir fastapi uvicorn pandas openai

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
