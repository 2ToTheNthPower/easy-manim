#Python based dockerfile
FROM python:3.12

# Set the working directory in the container
WORKDIR /frontend

# Copy the dependencies file to the working directory
COPY requirements.txt .

# Install any dependencies
RUN pip install -r requirements.txt

# Copy the content of the local src directory to the working directory
COPY . .

# Specify the command to run on container start
CMD [ "streamlit", "run", "main.py", "--server.port=8501", "--server.address=0.0.0.0" ]
