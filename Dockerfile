# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the current directory contents into the container at /usr/src/app
COPY . .

RUN pip install --no-cache-dir flask flask-socketio flask-httpauth eventlet

EXPOSE 5000

ENV FLASK_APP=server.py
ENV FLASK_RUN_HOST=0.0.0.0

# Run server.py when the container launches
CMD ["flask", "run"]
