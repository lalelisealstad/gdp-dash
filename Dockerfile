# Use the official Python base image
FROM python:3.12.4

# Set the working directory
WORKDIR /app

# Copy Poetry files first to leverage Docker caching
COPY pyproject.toml poetry.lock ./

# Install Poetry (using the recommended method)
RUN curl -sSL https://install.python-poetry.org | python3 -

# Add Poetry to the PATH
ENV PATH="/root/.local/bin:$PATH"

# Install the project dependencies using Poetry
RUN poetry install --no-interaction --no-ansi --no-root

# Copy the application code
COPY app.py ./app.py
COPY src/ ./src/
COPY assets/ ./assets/

# Expose port 8080
EXPOSE 8080

# Specify the command to run the app
CMD ["poetry", "run", "python", "app.py", "--host=0.0.0.0", "--port=8080"]
