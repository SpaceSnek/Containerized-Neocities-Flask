# syntax=docker/dockerfile:1
# Small python/apline image for running the app 
FROM python:3.9-alpine
# Set the working directory to /app
WORKDIR /app
# Copy the requirments.txt into the containe
COPY requirements.txt .
# Run the install against the requirements.txt file
RUN pip3 install --no-cache-dir -r requirements.txt
# Copy the current directory contents into the container at /app
COPY . .
# Make port 5000 available to the world outside this container
EXPOSE 5000
# define the containers environments variables
CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0"]