# Stage 1: Build stage
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Expose the port
EXPOSE 8080

# Command to run the application
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080"]
