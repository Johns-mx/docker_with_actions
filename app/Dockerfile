#>> Use a base image with Python
FROM python:latest
#FROM python:alpine3.12

#>> Set the working directory inside the container
WORKDIR /app

ENV PYTHONPATH "${PYTHONPATH}:/app"

#>> Copy the required dependencies
COPY requirements.txt .

#>> Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

#>> Copy all application code
COPY . .

#>> Command to run your application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
