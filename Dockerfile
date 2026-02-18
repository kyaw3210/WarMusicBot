FROM python:3.10-slim-bullseye

RUN apt-get update && apt-get install -y ffmpeg nodejs npm && apt-get clean

COPY . /app
WORKDIR /app

RUN pip3 install --no-cache-dir --upgrade -r requirements.txt

CMD ["python3", "main.py"]
