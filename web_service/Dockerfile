# Use the official Python image as the base image
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /service

# Copy the dependencies file to the working directory
COPY requirements.txt /service/

# Install any required dependencies
RUN pip install -r requirements.txt

# Copy the content of the local src directory to the working directory
COPY . /service/

# Move working directory to src
WORKDIR /service/src

# Expose the port that your FastAPI application will run on
EXPOSE 8888

# Define the command to run your streamlit application
CMD ["python", "app.py"]
