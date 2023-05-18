# Use an official Python runtime as a parent image
FROM python:3.9-buster

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container
COPY . /app

# Install required packages
RUN pip install aiohttp==3.8.4 \
    aiosignal==1.3.1 \
    async-timeout==4.0.2 \
    attrs==23.1.0 \
    certifi==2023.5.7 \
    charset-normalizer==3.1.0 \
    click==8.1.3 \
    frozenlist==1.3.3 \
    gTTS==2.3.2 \
    idna==3.4 \
    multidict==6.0.4 \
    numpy==1.24.3 \
    openai==0.27.6 \
    playsound==1.2.2 \
    PyAudio==0.2.13 \
    PyQt6==6.5.0 \
    PyQt6-Qt6==6.5.0 \
    PyQt6-sip==13.5.1 \
    PySide6==6.5.0 \
    PySide6-Addons==6.5.0 \
    PySide6-Essentials==6.5.0 \
    requests==2.30.0 \
    shiboken6==6.5.0 \
    simpleaudio==1.0.4 \
    SpeechRecognition==3.10.0 \
    tqdm==4.65.0 \
    urllib3==2.0.2 \
    yarl==1.9.2

# Make port 80 available to the world outside the container

# Run app.py when the container launches
CMD ["python", "./main.py"]
