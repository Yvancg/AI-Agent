# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt ./

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . .

# Make port 80 available to the world outside this container
EXPOSE 80

# Add a health check
HEALTHCHECK --interval=30s --timeout=10s --retries=3 CMD ["curl", "http://localhost:80/health"] || exit 1

# Set the entrypoint to the Python script
ENTRYPOINT ["python", "./agent.py"]