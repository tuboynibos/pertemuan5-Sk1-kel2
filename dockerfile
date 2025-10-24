FROM python:3.11-slim

# faster installs
ENV PIP_NO_CACHE_DIR=1
WORKDIR /app

# install deps
RUN pip install --upgrade pip && \
    pip install flask prometheus_client gunicorn

# copy code
COPY app.py /app/app.py

EXPOSE 5000
# use gunicorn for prod-ish run
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]
