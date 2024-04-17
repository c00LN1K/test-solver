# Use an official Python runtime as a parent image
FROM postgres:latest

# Set the working directory in the container to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Make port 5432 available to the world outside this container
EXPOSE 5432

# Define environment variable
ENV POSTGRES_USER myuser
ENV POSTGRES_PASSWORD mypassword
ENV POSTGRES_DB mydatabase

# Run the command to start PostgreSQL
CMD ["postgres"]