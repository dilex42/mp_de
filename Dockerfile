FROM python:3.9-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED=1

# Adding backend directory to make absolute filepaths consistent across services
WORKDIR /app

# Install Python dependencies

RUN apt-get update && apt-get install -y libpq-dev gcc

COPY requirements.txt /app
RUN pip install -r requirements.txt

RUN apt-get autoremove -y gcc
# Add the rest of the code
COPY . /app

CMD python main.py
