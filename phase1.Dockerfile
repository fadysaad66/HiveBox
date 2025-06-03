# Use Python slim image (smaller size)
FROM python:3.11-slim

# Set working directory inside the container
WORKDIR /app

# Copy the local Python script to the container
COPY . .

RUN pip install flask  # Installs Flask in the container



# Set the default command to run the script
CMD ["python", "hivebox.py"]
