# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Upgrade pip
RUN pip install --upgrade pip

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Install any needed extra packages specified in notification_config/notifiation_requirements.txt
RUN pip install --no-cache-dir -r notification_config/notification_requirements.txt

# Define entry point
ENTRYPOINT ["sh", "entrypoint.sh"]