# Dockerfile
FROM python:alpine3.7
COPY . /project
WORKDIR /project
RUN pip install -r requirements.txt
RUN pip install "uvicorn[standard]"
CMD ["uvicorn"  , "app:app"]