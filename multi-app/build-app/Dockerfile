FROM python:3.8-slim-buster

WORKDIR /app
RUN pip install flask
COPY app.py /app

EXPOSE 5001
CMD ["python", "app.py"]

