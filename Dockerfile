# Use an official Python runtime as a parent image
FROM python:3.9


WORKDIR /app


ADD . /app

RUN pip install --no-cache-dir -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 80

# Define environment variable
ENV MYSQL_HOST=localhost \
    MYSQL_USER=root \
    MYSQL_PASSWORD=password \
    MYSQL_DB=test_db

# Install Alembic
RUN pip install alembic

# Copy Alembic configuration
COPY alembic.ini /app/alembic.ini

# Create a volume for storing Alembic migrations
VOLUME /app/alembic


# Install Alembic
RUN pip install alembic

# Run Alembic migrations and start FastAPI app
CMD bash -c "alembic upgrade head && uvicorn main:app --host 0.0.0.0 --port 80"