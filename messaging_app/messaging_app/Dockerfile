# base image
FROM python:3.12

# work directory
WORKDIR /app

#install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# django default port.
EXPOSE 8000 

# Run the app
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]