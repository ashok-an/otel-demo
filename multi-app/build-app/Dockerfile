FROM python:3.8-slim-buster

WORKDIR /app
COPY requirements.txt /app
RUN pip install -r requirements.txt
COPY app.py /app

EXPOSE 5001
CMD ["python", "app.py"]

