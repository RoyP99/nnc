# Use the official Python 3.10 image as the base image
# FROM python:3.10
# Use node 20.5.0 as base image, this also contains python 3.11.2
FROM node:20.5.0

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file to the working directory
COPY requirements.txt .

# install pip
ENV PYTHON_PIP_VERSION=24.0
ENV PYTHON_GET_PIP_URL=https://github.com/pypa/get-pip/raw/dbf0c85f76fb6e1ab42aa672ffca6f0a675d9ee4/public/get-pip.py
ENV PYTHON_GET_PIP_SHA256=dfe9fd5c28dc98b5ac17979a953ea550cec37ae1b47a5116007395bfacff2ab9
RUN /bin/sh -c set -eux; wget -O get-pip.py "$PYTHON_GET_PIP_URL"; echo "$PYTHON_GET_PIP_SHA256 *get-pip.py" | sha256sum -c -; export PYTHONDONTWRITEBYTECODE=1; python3 get-pip.py --disable-pip-version->

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt --break-system-packages

# Copy the rest of the application code to the working directory
COPY . .

# change to vue-client
WORKDIR /app/vue-client

# and install node js libraries
RUN npm install

# and build the vue app
RUN npm run build

# change back to working directory
WORKDIR /app

# Expose the port on which the Flask app will run
EXPOSE 5000

# Specify the command to run the application
CMD [ "python3", "main.py" ]