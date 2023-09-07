# Use the official Python image as the base image
FROM python:3.10-slim

# Set environment variables
ENV DATABASE_PATH=/database/product.db

# Create docker volume for database
VOLUME /database

# Set the working directory inside the container
WORKDIR /service

# Copy the dependencies file to the working directory
COPY requirements.txt /service/

# Install any required dependencies
RUN pip install -r requirements.txt

# Copy the content of the local src directory to the working directory
COPY . /service/

# Expose the port that your FastAPI application will run on
EXPOSE 8002

# Define the command to run your FastAPI application with Uvicorn
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8002"]
