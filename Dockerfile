# Use a Python base image with required system dependencies
FROM python:3.9-slim

# Install system dependencies for numpy and pandas
RUN apt-get update && apt-get install -y \
    build-essential \
    gfortran \
    libopenblas-dev \
    liblapack-dev

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements.txt file to install dependencies
COPY requirements.txt .

# Install Python dependencies
RUN python3 -m venv venv && . venv/bin/activate && pip install --upgrade pip && pip install -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the port Flask runs on
EXPOSE 8080

# Run the application
CMD ["python", "main.py"]
