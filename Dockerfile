FROM python:3.10.8

WORKDIR /chefbot

# Install system dependencies for PyAudio, PySide6, and PyGObject
RUN apt-get update && \
    apt-get install -y portaudio19-dev libgl1-mesa-glx libgirepository1.0-dev && \
    apt-get clean

COPY requirements.txt .

RUN pip install -r requirements.txt
RUN pip install --upgrade pip

COPY ./recipes ./recipes

CMD ["python", "./main.py"]