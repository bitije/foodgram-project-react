FROM python:3.11-slim

WORKDIR /app

COPY . .

COPY requirements.txt ./ 

RUN pip install -U pip

RUN pip install -r ./requirements.txt --no-cache-dir --no-input 

CMD ["gunicorn", "foodgram.wsgi:application", "--bind", "0:8000" ]