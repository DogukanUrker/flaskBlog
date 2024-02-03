# Use the official Python image as the base image
# This image contains the Python interpreter and the standard library
FROM python:3.12.1

# Set the working directory to /app
# This is where the app code and files will be stored inside the container
WORKDIR /app

# Copy the requirements file from the current directory to the /app directory
# This file lists the Python packages that the app depends on
COPY requirements.txt .

# Install the dependencies using pip
# This will ensure that the app has all the necessary modules to run
RUN pip install -r requirements.txt

# Copy the rest of the code and files from the current directory to the /app directory
# This will include the app.py file and any other files needed by the app
COPY . .

# Expose the port 5000 to the outside world
# This is the port that the app listens on and accepts connections from
EXPOSE 5000

# Define the command to run the app when the container starts
# This will execute the app.py file using the Python interpreter
CMD ["python", "app.py"]
