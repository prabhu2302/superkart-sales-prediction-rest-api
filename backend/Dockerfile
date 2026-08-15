# Use a lightweight Python 3.9 base image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy all backend files into the container
COPY . .

# Install the Python dependencies
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Start the Flask app with Gunicorn on port 7860
#  -w 4          : 4 worker processes
#  -b 0.0.0.0    : listen on all interfaces
#  app:superkart_api : module `app`, Flask object `superkart_api`
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:7860", "app:superkart_api"]
