# Dockerfile
FROM python:3.9
COPY . /project
WORKDIR /project
RUN pip install -r requirements.txt
RUN pip install "uvicorn[standard]"
EXPOSE 8080
CMD ["uvicorn"  , "app:app"]
