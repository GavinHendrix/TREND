# Use a Python image
FROM python:3.12

# Set the working directory
WORKDIR /app

# Copy the project files into the container
COPY . /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libpq-dev gcc && \
    rm -rf /var/lib/apt/lists/*

# Create a virtual environment
RUN python -m venv /venv

# Activate virtual environment and install Python dependencies
ENV PATH="/venv/bin:$PATH"
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Expose the Flask port
EXPOSE 5050

# Set the entry point to run.py
CMD ["python", "run.py"]
