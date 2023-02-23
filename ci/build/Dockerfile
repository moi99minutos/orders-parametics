# Dockerfile
FROM python:3.11-slim
ENV PYTHONUNBUFFERED True
ENV APP_HOME /project
COPY . /project
WORKDIR /project
ENV PORT 8080
RUN pip install -r requirements.txt
RUN pip install "uvicorn[standard]"
# CMD exec uvicorn app:app --host 0.0.0.0 --port ${PORT} --workers 1
EXPOSE 8080
CMD exec gunicorn --bind :$PORT --workers 1 --worker-class uvicorn.workers.UvicornWorker  --threads 8 app:app

