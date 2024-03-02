# Use a Python 3.11 base image
FROM python:3.11

# Create a working directory inside the container
WORKDIR /app

# Copy your Python code and requirements to the working directory
COPY . .

# Install Python dependencies
RUN pip install -r requirements.txt

# Default command to run the Python application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]