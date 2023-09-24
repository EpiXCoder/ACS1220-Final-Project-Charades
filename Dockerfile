# Use an official Python runtime as the parent image
FROM python:3.8-slim

# Set the working directory in the container to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY requirements.txt requirements.txt

# Install the Python dependencies
RUN pip install -r requirements.txt

# Copy the rest of the application's code into the container
COPY . .

# Set environment variables for Flask
ENV FLASK_APP=app.py
ENV FLASK_ENV=development

# Inform Docker that the container listens on the specified port at runtime
EXPOSE 5003

# Define the command to run the application using the Flask built-in server
CMD ["python", "app.py"]
