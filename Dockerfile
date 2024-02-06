FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the current directory contents into the container at /usr/src/app
COPY . .

RUN pip install --no-cache-dir flask flask-socketio flask-httpauth eventlet gunicorn

EXPOSE 5000

CMD ["gunicorn", "-k", "eventlet", "-w", "1", "--threads", "5", "-b", "0.0.0.0:5000", "server:app"]
