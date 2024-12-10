# Sample Dockerfile for Splunk-Terraform-Python project
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy application code
COPY . .

# Install dependencies
RUN pip install -r requirements.txt

# Set the default command
CMD ["python", "main.py"]
