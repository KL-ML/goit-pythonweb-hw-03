FROM python:3.12-slim

# Install pipenv
RUN pip install pipenv

# Set working directory
WORKDIR /app

# Copy Pipfile and Pipfile.lock
COPY Pipfile Pipfile.lock ./

# Copy application code
COPY . .

# Install dependencies
RUN pipenv install --system --deploy

EXPOSE 3000

# Run the application
ENTRYPOINT ["python3", "server.py"]
