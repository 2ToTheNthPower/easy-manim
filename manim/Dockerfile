# Dockerfile based on manim container
FROM manimcommunity/manim:stable

USER root

# Install xdg-utils
RUN apt-get update && apt-get install -y xdg-utils w3m

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install the requirements
RUN pip install -r requirements.txt

# Copy the source code
COPY . .

# Expose the port
EXPOSE 8000

# Start the FastAPI server
ENTRYPOINT [ "python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
