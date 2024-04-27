# Dockerfile based on manim container
FROM manimcommunity/manim:stable

USER root
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
