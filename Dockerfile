FROM python:3.12.3-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common 

COPY . .

RUN pip3 install -r requirements.txt

EXPOSE 80

#HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["rom_video_game", "run", "app.py", "--server.port=80", "--server.address=0.0.0.0"]