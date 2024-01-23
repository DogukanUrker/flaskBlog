# Use the official Python image as the base image
FROM python:3.12

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install the dependencies
RUN pip install -r requirements.txt

# Copy the rest of the code
COPY . .

# Expose the port
EXPOSE 5000

# Define the command to run the app
CMD ["python", "app.py"]
