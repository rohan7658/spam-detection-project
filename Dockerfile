# Use an official Python runtime as the base image
FROM python:3.9-slim
#FROM python:3.9.18-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file
COPY requirements.txt /app/

# Install the dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project (including the 'Spam Detection' folder) into the container
COPY . /app/

# Expose the port Django will run on
EXPOSE 8000

# Default command to run the Django development server
CMD ["python", "Spam Project/manage.py", "runserver", "0.0.0.0:8000"]
