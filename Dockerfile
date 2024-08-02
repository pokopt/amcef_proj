# Use the official Python image from the Docker Hub
FROM python:3.12-slim

# Set environment variables to avoid buffering
ENV PYTHONUNBUFFERED=1

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt /app/

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . /app/

# Expose port 8000 to the outside world
EXPOSE 8000

# Copy the entrypoint script and make it executable
COPY docker_entry.sh /app/
RUN chmod +x /app/docker_entry.sh
# Set the entrypoint to the custom script
ENTRYPOINT ["/app/docker_entry.sh"]

# Define the command to run the application
# CMD ["gunicorn", "--bind", "0.0.0.0:8000", "amcef_proj.wsgi:application"]