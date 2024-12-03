# Python Runtime as Parent Image
FROM python:3.12

# Set Working Directory
WORKDIR /app

# Copy Only Necessary Files to Leverage Docker Caching
COPY requirements.txt Makefile ./

# Install System Dependencies for PyInstaller
RUN apt-get update && apt-get install -y \
    build-essential \
    libssl-dev \
    libffi-dev \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Global PyInstaller Install
RUN pip install pyinstaller

# Check Python Version and Install Dependencies via Makefile
RUN make check-python install

# Copy Entire Project to Container
COPY . .

# Build Executable
RUN make build-docker

# Expose Port
EXPOSE 5050

# Set Default Command to Run Executable
CMD ["make run"]