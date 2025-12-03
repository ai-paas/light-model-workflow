# 베이스 이미지로 python:3.10-slim 사용
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /app

# Copy only the Pipfile and Pipfile.lock to leverage Docker cache
COPY Pipfile Pipfile.lock ./

RUN pip install --upgrade pip
RUN pip install pipenv
RUN pipenv install --deploy --system

COPY . .
EXPOSE 5000

CMD ["python3.10", "-m", "uvicorn", "app.main:app", "--reload",  "--host=0.0.0.0", "--port=5000"]
