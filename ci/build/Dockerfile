# Dockerfile
FROM python:3.9-slim@sha256:980b778550c0d938574f1b556362b27601ea5c620130a572feb63ac1df03eda5 
ENV PYTHONUNBUFFERED True
ENV APP_HOME /project
COPY . /project
WORKDIR /project
ENV PORT 8080
RUN pip install -r requirements.txt
RUN pip install "uvicorn[standard]"
CMD exec gunicorn --bind :$PORT --workers 1 --worker-class uvicorn.workers.UvicornWorker  --threads 8 main:app

