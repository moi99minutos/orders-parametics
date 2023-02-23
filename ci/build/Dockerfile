# Dockerfile
FROM python:3.9
COPY . /project
WORKDIR /project
RUN pip install -r requirements.txt
RUN pip install "uvicorn[standard]"
CMD ["uvicorn"  , "app:app"]
