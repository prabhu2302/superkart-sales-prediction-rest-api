# Use a lightweight Python 3.9 base image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy all frontend files into the container
COPY . .

# Install the Python dependencies
RUN pip3 install -r requirements.txt

# Run the Streamlit app on port 8501, reachable from outside the container.
# XSRF protection is disabled to allow CSV uploads for batch prediction.
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0", "--server.enableXsrfProtection=false"]
