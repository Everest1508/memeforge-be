# Use official Python image
FROM python:3.10

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /code

# Install dependencies
COPY requirements.txt /code/
RUN pip install -r requirements.txt

# Copy project
COPY . /code/

# Collect static files
RUN python manage.py collectstatic --noinput

# Expose port
EXPOSE 7860

# Run server
CMD ["python", "manage.py", "runserver", "0.0.0.0:7860"]
