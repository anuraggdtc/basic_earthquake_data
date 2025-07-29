# Base Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy files
COPY main.py .

# run 
RUN pip install pandas
RUN pip install requests

# Run when container start
CMD ["python", "main.py"]