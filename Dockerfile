# Use the official Python image as the base image
FROM python:3.10

# Set the working directory in the container
WORKDIR /app

# Copy the application files to the container's working directory
COPY . /app

# Install the project dependencies
RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi

# Set the entry point for the container
CMD ["streamlit", "run", "streamlit_agent"]
