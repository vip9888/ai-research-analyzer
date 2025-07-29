# Base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy everything needed from root project directory
COPY requirements.txt .
COPY backend ./backend
COPY frontend ./frontend
COPY start.sh .

# Install dependencies
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# Expose backend and frontend ports
EXPOSE 8000 8501

# Start both services
CMD ["bash", "start.sh"]
