FROM python:3.10.3-slim-bullseye

# Install system dependencies
RUN apt-get -y update && \
    apt-get install -y --fix-missing \
    build-essential \
    cmake \
    gfortran \
    git \
    wget \
    curl \
    graphicsmagick \
    libgraphicsmagick1-dev \
    libatlas-base-dev \
    libavcodec-dev \
    libavformat-dev \
    libgtk2.0-dev \
    libjpeg-dev \
    liblapack-dev \
    libswscale-dev \
    pkg-config \
    python3-dev \
    python3-numpy \
    software-properties-common \
    zip \
    && apt-get clean && rm -rf /tmp/* /var/tmp/*

# Install dlib
RUN cd ~ && \
    mkdir -p dlib && \
    git clone -b 'v19.9' --single-branch https://github.com/davisking/dlib.git dlib/ && \
    cd  dlib/ && \
    python3 setup.py install --yes USE_AVX_INSTRUCTIONS

# Install MongoDB
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gnupg \
    && wget -qO - https://www.mongodb.org/static/pgp/server-5.0.asc | apt-key add - \
    && echo "deb http://repo.mongodb.org/apt/debian bullseye/mongodb-org/5.0 main" | tee /etc/apt/sources.list.d/mongodb-org-5.0.list \
    && apt-get update && \
    apt-get install -y mongodb-org \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set up data directory with proper permissions
RUN mkdir -p /data/db && \
    chown -R mongodb:mongodb /data/db

WORKDIR /face_recognition

# Copy application files
COPY . .

# Install Python dependencies
RUN pip install -r requirements.txt

# Set up environment variables for MongoDB connection
ENV MONGO_HOST localhost
ENV MONGO_PORT 27017
ENV MONGO_DB your_database_name

# Start MongoDB and run the application
CMD mongod --fork --logpath /var/log/mongodb.log && python server.py
