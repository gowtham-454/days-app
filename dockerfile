# Use the official Python image from the Docker Hub
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the required Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code and other necessary files into the container
COPY app.py .
COPY checked_days.json .
COPY templates/index.html ./templates/

# Expose the port that Flask will run on
EXPOSE 5000

# Command to run your Flask application
CMD ["python", "app.py"]