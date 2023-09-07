FROM python:3.10-slim

# Create a new user with a specific username and user ID (UID)
RUN useradd -m -u 1000 user

# Set the user as the default user for the container
USER user

# Set the working directory inside the container
WORKDIR /service

# Copy the dependencies file to the working directory
COPY requirements.txt /service/

# Install any required dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the content of the local src directory to the working directory
COPY . /service/

# Move working directory to src
WORKDIR /service/src

# Expose the port that your FastAPI application will run on
EXPOSE 8888

# Add a healthcheck to monitor the status of your application
HEALTHCHECK --interval=30s --timeout=3s \
    CMD curl -f http://localhost:8888 || exit 1

# Define the command to run your streamlit application
CMD ["python", "app.py"]
