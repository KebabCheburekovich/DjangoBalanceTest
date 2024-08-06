FROM python:3.11-slim

WORKDIR /app_back
COPY requirements.txt /app_back/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app_back/
RUN python3 manage.py makemigrations
RUN python3 manage.py migrate
#RUN python3 manage.py createsuperuser --noinput

EXPOSE 8000

CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
