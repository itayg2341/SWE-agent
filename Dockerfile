FROM python:3.9

# Set the working directory
WORKDIR /app

# Install nodejs
RUN apt update && \
    apt install -y nodejs npm && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install Docker CLI using the official Docker installation script


# Copy the application code
# Do this last to take advantage of the docker layer mechanism
COPY . /app

# Install Python dependencies
RUN pip install -e '.'

# Install react dependencies ahead of time
VOLUME /var/run/docker.sock:/var/run/docker.sock
RUN cd sweagent/frontend && npm install
