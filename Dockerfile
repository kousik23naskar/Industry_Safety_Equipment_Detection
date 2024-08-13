# Use a lightweight Python image as the base
FROM python:3.11-slim-buster

# Expose the Streamlit default port
EXPOSE 8501

# Install necessary system packages and clean up to keep the image slim
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    software-properties-common \
    git \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*
#to resolve ImportError: libGL.so.1 error, install libgl1-mesa-glx and libglib2, necessary for OpenCV to handle graphical processing
# Set the working directory inside the container
WORKDIR /Detectionapp

# Copy all the application files to the working directory
COPY . /Detectionapp

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set the entry point to start the Streamlit app
ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
