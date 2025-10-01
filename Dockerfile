FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY park_monitor.py .
COPY config.yaml .

# Create logs directory
RUN mkdir -p /app/logs

# Run the monitor
CMD ["python", "-u", "park_monitor.py"]